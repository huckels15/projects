import tensorflow as tf
import keras
import numpy as np
from argparse import ArgumentParser
import utils.backend as b
import utils.dataset_loader as ds
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers.legacy import Adam
from tflite_to_cmsis import tflite_to_cmsis_main as cm
from src.robustness_testing_pipeline.art.attacks.extraction.copycat_cnn_int8 import CopycatCNN_Int8
from src.robustness_testing_pipeline.art.estimators.classification.tensorflow_int8 import TensorFlowV2Classifier_Int8
from src.robustness_testing_pipeline.training.resnet.model_converter import representative_dataset_generator, convert_model
from src.robustness_testing_pipeline.training.mobilenet.convert_vww import run_conversion
from src.robustness_testing_pipeline.art.estimators.classification.tensorflow import TensorFlowV2Classifier
import src.robustness_testing_pipeline.theived_templates_cifar as cifar_models
import src.robustness_testing_pipeline.theived_templates_vww as vww_models
import datetime
import tensorflow_model_optimization as tfmot
from sklearn.model_selection import train_test_split

dt = datetime.datetime.today()
year = dt.year
month = dt.month
day = dt.day
hour = dt.hour
minute = dt.minute


def load_configs():
    parser = ArgumentParser(add_help=True)
    parser.add_argument("--dataset_id", type=str, default=None, help="dataset to use: cifar10 or vww")
    parser.add_argument("--batch_size_fit", type=int, default=32, help="number of samples to perturb")
    parser.add_argument("--batch_size_query", type=str, default=32, help="path to save the adversarial examples")
    parser.add_argument("--nb_epochs", type=float, default=100, help="")
    parser.add_argument("--nb_stolen", type=float, default=50000, help="")
    parser.add_argument("--num_classes", type=int, default=10, help="number of classes in target models")
    parser.add_argument("--target_int8", type=str, default=None, help="path to the int-8 QNN")
    parser.add_argument("--model_folder", type=str, default="/models", help="path to save thieved model")
    parser.add_argument("--theived_template", type=str, default="basic", help="theived model architecture")
    parser.add_argument("--qat", action='store_true')

    cfgs = parser.parse_args()

    # Check if any required argument is not set
    required_cfgs = ['dataset_id', 'num_classes', 'target_int8']
    for arg_name in required_cfgs:
        if getattr(cfgs, arg_name) is None:
            raise ValueError(f"Required argument {arg_name} is not set.")
        
    run_cfgs = vars(cfgs)

    return run_cfgs

@tf.function
def train_step(model, images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = tf.keras.losses.categorical_crossentropy(labels, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    return loss

@tf.function
def train_step_qat(model, images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = tf.keras.losses.categorical_crossentropy(labels, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    return loss


def main():
    # Step 1: Load configs
    cfgs = load_configs()

    if cfgs['dataset_id'] == 'cifar10':
        task = "cifar"
        input_shape = (32,32,3)
        if cfgs['theived_template'] == 'vgg': 
            thieved_model = cifar_models.create_vgg16()
            arch = 'vgg'
        elif cfgs['theived_template'] == 'lenet': 
            thieved_model = cifar_models.create_lenet()
            arch = 'lenet'
        elif cfgs['theived_template'] == 'alexnet': 
            thieved_model = cifar_models.create_alexnet()
            arch = 'alexnet'
        elif cfgs['theived_template'] == 'resnet': 
            thieved_model = cifar_models.create_resnet()
            arch = 'resnet'
        else: 
            thieved_model = cifar_models.create_basic()
            arch = 'basic'
    elif cfgs['dataset_id'] == 'vww':
        task = "vww"
        input_shape = (96,96,3)
        if cfgs['theived_template'] == 'vgg': 
            thieved_model = vww_models.create_vgg16()
            arch = 'vgg'
        elif cfgs['theived_template'] == 'lenet': 
            thieved_model = vww_models.create_lenet()
            arch = 'lenet'
        elif cfgs['theived_template'] == 'alexnet': 
            thieved_model = vww_models.create_alexnet()
            arch = 'alexnet'
        elif cfgs['theived_template'] == 'resnet': 
            thieved_model = vww_models.create_resnet()
            arch = 'resnet'
        elif cfgs['theived_template'] == 'mobilenet':
            thieved_model = vww_models.create_mobilenet()
            arch = 'mobilenet'
        else: 
            thieved_model = vww_models.create_basic()
            arch = 'basic'

    # Step 2: Load ANN/QNNs
    qnn_int8 = b.get_ml_quant_model(cfgs['target_int8'])
    scaler_int8, zp_int8 = b.get_input_quant_details(qnn_int8)
    art_classifier = TensorFlowV2Classifier_Int8(model=qnn_int8, clip_values=(0, 1),
                            nb_classes=cfgs['num_classes'], input_shape=input_shape,
				            loss_object=tf.keras.losses.CategoricalCrossentropy())

    # Step 3: Load dataset and generate .bin files
    if cfgs['dataset_id'] == 'cifar10':
        x_train_float, y_train = ds.get_cifar10_train_ds_f32()
        x_test_float, y_test = ds.get_cifar10_test_ds_f32()
    elif cfgs['dataset_id'] == 'vww':
        x_train_float, y_train = ds.get_vww_train_ds_f32()
        x_test_float, y_test = ds.get_vww_test_ds_f32()

    x_train_int8 = b.quantize_dataset_int8(x_train_float, scaler_int8, zp_int8)
    x_test_int8 = b.quantize_dataset_int8(x_test_float, scaler_int8, zp_int8)

    # Step 4: Evaluate classifier test examples
    accuracy = b.get_accuracy_quant_model(qnn_int8, x_test_int8, y_test)
    print("Int8 -> Accuracy on test examples: {}%".format(accuracy * 100) + "\n")

    # Step 5: Steal model
    attack = CopycatCNN_Int8(classifier=art_classifier, batch_size_fit=cfgs['batch_size_fit'],\
    batch_size_query=cfgs['batch_size_query'], nb_epochs=int(cfgs['nb_epochs']), nb_stolen=int(cfgs['nb_stolen']))
    thieved_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    thieved_classifier = TensorFlowV2Classifier(model=thieved_model, nb_classes=cfgs['num_classes'], input_shape=input_shape, train_step=train_step)
    stolen_model = attack.extract(x_train_float, y_train, thieved_classifier=thieved_classifier)

    stolen_name = f"stolen_{arch}_{task}_{year}{month:02d}{day:02d}_{hour:02d}{minute:02d}"
    stolen_model.model.save(f"src/robustness_testing_pipeline/models/fp_models/{stolen_name}.h5")

    if cfgs['qat']:
        x_train, x_train_qat, y_train_tmp, y_train_qat = train_test_split(x_train_float, y_train, test_size = 0.2)
        attack_qat = CopycatCNN_Int8(classifier=art_classifier, batch_size_fit=cfgs['batch_size_fit'],\
        batch_size_query=cfgs['batch_size_query'], nb_epochs=10, nb_stolen=len(x_train_qat))
        quantize_model = tfmot.quantization.keras.quantize_model
        q_aware_model = quantize_model(stolen_model.model)
        q_aware_model.compile(
            optimizer='adam',
            loss="categorical_crossentropy",
            metrics=['accuracy'],
        )
        qat_thieved_class = TensorFlowV2Classifier(model=q_aware_model, nb_classes=cfgs['num_classes'], input_shape=input_shape, train_step=train_step_qat)
        stolen_model_qat = attack_qat.extract(x_train_qat, y_train_qat, thieved_classifier=qat_thieved_class)
        test_loss, test_acc = stolen_model_qat.model.evaluate(x_test_float, y_test)
        preds_og = b.get_model_predictions(qnn_int8, x_test_int8)
        preds_qat = stolen_model_qat.model.predict(x_test_float)
        preds_qat_classes = np.argmax(preds_qat, axis=1)

        matching_predictions = np.sum(preds_og == preds_qat_classes)
        total_predictions = len(preds_og)

        fidelity = matching_predictions / total_predictions 
        print(f"QAT test acc: {test_acc * 100}%\nFidelity:{fidelity * 100}%")
        stolen_model_qat.model.save(f"src/robustness_testing_pipeline/models/qat_models/{stolen_name}_qat_test.h5")


    if cfgs['dataset_id'] == 'cifar10':
        convert_model(f"{stolen_name}.h5")
    elif cfgs['dataset_id'] == 'vww':
        run_conversion(f"{stolen_name}.h5")


    stolen_int8 = b.get_ml_quant_model(f"src/robustness_testing_pipeline/models/quant_models/{stolen_name}_quant.tflite")

    accuracy_train = b.get_accuracy_quant_model(stolen_int8, x_train_int8, y_train)
    print("Int8 -> Train Accuracy: {}%".format(accuracy_train * 100))

    # Step 6: Evaluate the classifiers
    accuracy = b.get_accuracy_quant_model(stolen_int8, x_test_int8, y_test)
    print("Int8 -> Test Accuracy: {}%".format(accuracy * 100))

    # Step 7: Get predictions from both the original and stolen model
    preds_original = b.get_model_predictions(qnn_int8, x_test_int8)  # Original model predictions
    preds_stolen = b.get_model_predictions(stolen_int8, x_test_int8)  # Stolen model predictions

    # Step 8: Compare the predictions and calculate the ratio of matching predictions
    matching_predictions = np.sum(preds_original == preds_stolen)  # Count matching predictions
    total_predictions = len(preds_original)  # Total number of predictions

    fidelity = matching_predictions / total_predictions  # Ratio of matching predictions
    print(f"Fidelity: {fidelity * 100}%")

if __name__ == '__main__':
    main()
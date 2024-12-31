import tensorflow as tf
import numpy as np
from argparse import ArgumentParser
import utils.backend as b
import utils.dataset_loader as ds
from tflite_to_cmsis import tflite_to_cmsis_main as cm
from src.robustness_testing_pipeline.art.attacks.evasion.projected_gradient_descent.projected_gradient_descent import ProjectedGradientDescent
from src.robustness_testing_pipeline.art.estimators.classification import TensorFlowV2Classifier
from tensorflow_model_optimization.quantization.keras import quantize_scope


def load_configs():
    parser = ArgumentParser(add_help=True)
    parser.add_argument("--dataset_id", type=str, default=None, help="dataset to use: cifar10, vww, or coffee")
    parser.add_argument("--dataset_size", type=int, default=1000, help="number of samples to perturb")
    parser.add_argument("--num_classes", type=int, default=10, help="number of classes in target models")
    parser.add_argument("--ann_float", type=str, default=None, help="path to the floating-point ANN")
    parser.add_argument("--qnn_int16", type=str, default=None, help="path to the int-16 QNN")
    parser.add_argument("--qnn_int8", type=str, default=None, help="path to the int-8 QNN")
    parser.add_argument("--logs_folder", type=str, default=None, help="path to save the adversarial examples")
    parser.add_argument("--pgd_eps", type=str, default=0.008, help="")
    parser.add_argument("--pgd_num_random_init", type=int, default=20, help="")
    parser.add_argument("--pgd_max_iter", type=int, default=20, help="")

    cfgs = parser.parse_args()

    # Check if any required argument is not set
    required_cfgs = ['dataset_id', 'num_classes', 'ann_float']
    for arg_name in required_cfgs:
        if getattr(cfgs, arg_name) is None:
            raise ValueError(f"Required argument {arg_name} is not set.")
        
    run_cfgs = vars(cfgs)
    pgd_eps = run_cfgs['pgd_eps'].split(",")
    run_cfgs['pgd_eps'] = np.array(pgd_eps, dtype=float)

    return run_cfgs


def main():
    # Step 1: Load configs
    cfgs = load_configs()

    if cfgs['dataset_id'] == 'cifar10':
        input_shape = (32,32,3)
    elif cfgs['dataset_id'] == 'vww':
        input_shape = (96,96,3)

    # Step 2: Load ANN/QNNs1
    with quantize_scope():
        ann_f32 = tf.keras.models.load_model(cfgs['ann_float'])
    art_classifier = TensorFlowV2Classifier(model=ann_f32, clip_values=(0, 1),
                            nb_classes=cfgs['num_classes'], input_shape=input_shape,
				            loss_object=tf.keras.losses.CategoricalCrossentropy())

    # Step 3: Load dataset and generate .bin files
    if cfgs['dataset_id'] == 'cifar10':
        x_test_float, y_test = ds.get_cifar10_test_ds_f32()
    elif cfgs['dataset_id'] == 'vww':
        x_test_float, y_test = ds.get_vww_test_ds_f32()

    x_test_float, y_test = x_test_float[0:cfgs['dataset_size']], y_test[0:cfgs['dataset_size']]
    # cm.generate_dataset_bin(x_test_float, cfgs['logs_folder'], 'x_test_float.bin')
    # cm.generate_dataset_bin(x_test_int16, cfgs['logs_folder'], 'x_test_int16.bin')
    # cm.generate_dataset_bin(x_test_int8, cfgs['logs_folder'], 'x_test_int8.bin')
    # cm.generate_labels_bin(y_test, cfgs['logs_folder'], 'labels.bin')

    # Step 4: Evaluate classifiers on benign test examples
    accuracy = b.get_accuracy_f32(ann_f32, x_test_float, y_test)
    print("Float -> Accuracy on benign test examples: {}%".format(accuracy * 100))
    # accuracy = b.get_accuracy_quant_model(qnn_int16, x_test_int16, y_test)
    # print("Int16 -> Accuracy on benign test examples: {}%".format(accuracy * 100) + "\n")
    # accuracy = b.get_accuracy_quant_model(qnn_int8, x_test_int8, y_test)
    # print("Int8 -> Accuracy on benign test examples: {}%".format(accuracy * 100) + "\n")

    # Step 5: Generate adversarial test examples
    for i, max_linf in enumerate(cfgs['pgd_eps']):
        print("MAXIMUM LInf: " + str(max_linf))

        attack = ProjectedGradientDescent(estimator=art_classifier, eps=max_linf, eps_step=max_linf/10.0,
                                        num_random_init=cfgs['pgd_num_random_init'], max_iter=cfgs['pgd_max_iter'], batch_size=1)
        x_adv_float = attack.generate(x=x_test_float, y=y_test)
        x_adv_float = np.array(x_adv_float).astype(np.float32)
        # x_adv_int16 = b.quantize_dataset_int16(x_adv_float, scaler_int16, zp_int16)
        # x_adv_int8 = b.quantize_dataset_int8(x_adv_float, scaler_int8, zp_int8)

        # Step 6: Evaluate the classifiers on adversarial test examples
        accuracy = b.get_accuracy_f32(ann_f32, x_adv_float, y_test)
        print("Float -> Accuracy: {}%".format(accuracy * 100))
        # accuracy = b.get_accuracy_quant_model(qnn_int16, x_adv_int16, y_test)
        # print("Int16 -> Accuracy: {}%".format(accuracy * 100))
        # accuracy = b.get_accuracy_quant_model(qnn_int8, x_adv_int8, y_test)
        # print("Int8 -> Accuracy: {}%".format(accuracy * 100))

        # Step 7: Calculate distance metrics
        l0_max, l0_avg = b.get_l0_norm(x_test_float, x_adv_float)
        l1_max, l1_avg = b.get_l1_norm(x_test_float, x_adv_float)
        l2_max, l2_avg = b.get_l2_norm(x_test_float, x_adv_float)
        linf_max, linf_avg = b.get_linf_norm(x_test_float, x_adv_float)
        print("L0 distortion -> Max: " + str(l0_max) + " -> Avg: " + str(l0_avg))
        print("L1 distortion -> Max: " + str(l1_max) + " -> Avg: " + str(l1_avg))
        print("L2 distortion -> Max: " + str(l2_max) + " -> Avg: " + str(l2_avg))
        print("Linf distortion -> Max: " + str(linf_max) + " -> Avg: " + str(linf_avg) + "\n")

        # Step 8: Save adversarial dataset to .bin file
        # cm.generate_dataset_bin(x_adv_float, cfgs['logs_folder'], 'adv_float_' + str(i) + '.bin')
        # cm.generate_dataset_bin(x_adv_int16, cfgs['logs_folder'], 'adv_int16_' + str(i) + '.bin')
        # cm.generate_dataset_bin(x_adv_int8, cfgs['logs_folder'], 'adv_int8_' + str(i) + '.bin')


if __name__ == '__main__':
    main()
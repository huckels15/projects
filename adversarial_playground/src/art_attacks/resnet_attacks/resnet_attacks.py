import tensorflow as tf
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent as PGD, DeepFool, SquareAttack as Square
from art.estimators.classification import KerasClassifier
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
tf.compat.v1.disable_eager_execution()
import pandas as pd
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def load_data(sample_size=100):
    '''
    Function to load a small subset of the data and return only the test data generator.
    '''
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator()

    data = pd.read_csv("data/dvc_store_csvs_hmnist_28_28_RGB.csv")
    y = data['label']
    X = data.drop(columns=['label'])

    X = X.values.reshape(-1, 28, 28, 3)

    if sample_size > 0:
        sampled_indices = np.random.choice(len(X), sample_size, replace=False)
        X = X[sampled_indices]
        y = y.iloc[sampled_indices]

    y = to_categorical(y, num_classes=7)

    with tf.compat.v1.Session() as sess:
        X_resized = sess.run(tf.image.resize(X, (224, 224)))

    test_gen = test_datagen.flow(X_resized, y, batch_size=sample_size)
    
    return test_gen


def plot_samples(num_samples, x_test, x_test_adv, y_test, predictions_adv):
    '''
    Function to plot a sample before and after adversarial perturbations.
    '''
    class_map = {
        0: 'Melanocytic nevi',
        1: 'Melanoma',
        2: 'Benign keratosis',
        3: 'Basal cell carcinoma',
        4: 'Actinic keratoses',
        5: 'Vascular lesions',
        6: 'Dermatofibroma'
    }
    
    for i in range(num_samples):
        true_label = class_map[np.argmax(y_test[i])]
        adv_pred_label = class_map[np.argmax(predictions_adv[i])]
        
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        
        ax[0].imshow(x_test[i].astype(np.uint8))
        ax[0].set_title(f"Original\nTrue: {true_label}", fontsize=12, color="green")
        ax[0].axis('off')
        
        ax[1].imshow(x_test_adv[i].astype(np.uint8))
        ax[1].set_title(f"Adversarial\nTrue: {true_label}\nPred: {adv_pred_label}", fontsize=12, color="red")
        ax[1].axis('off')
        
        fig.suptitle(f"Example {i + 1}", fontsize=14, fontweight="bold")
        plt.savefig(f"figures/example_1_original_vs_adversarial.png")
        path = f"figures/example_1_original_vs_adversarial.png"
        return path

def parse_args():
    '''
    Function to parse command line arguments to choose attack and parameters
    for the attack.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fgsm", 
        action="store_true", 
        help="Run FGSM attack"
    )
    parser.add_argument(
        "--pgd", 
        action="store_true", 
        help="Run PGD attack"
    )
    parser.add_argument(
        "--deepfool", 
        action="store_true", 
        help="Run DeepFool attack"
    )
    parser.add_argument(
        "--square", 
        action="store_true", 
        help="Run Square attack"
    )
    parser.add_argument(
        "--eps", 
        type=str,
        default="0.2", 
        help="Run Square attack"
    )
    parser.add_argument(
        "--eps_step", 
        type=str,
        default="0.01", 
        help="Run Square attack"
    )
    parser.add_argument(
        "--max_iter", 
        type=str,
        default="50", 
        help="Run Square attack"
    )

    args = parser.parse_args()
    run_args = vars(args)

    return args, run_args

def run(args, run_args):
    '''
    Function to run adversarial examaple attacks on resnet model.
    '''
    test_gen = load_data()
    custom_objects = {"Adam": Adam}

    model = tf.keras.models.load_model("models/trainedResnet_20241016_2143.h5", custom_objects=custom_objects, compile=False)
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    min_pixel_value, max_pixel_value = 0.0, 255.0
    classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

    x_test, y_test = next(test_gen) 
    predictions = classifier.predict(x_test)
    accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)

    if args.fgsm:
        attack = FastGradientMethod(estimator=classifier, eps=float(run_args['eps']))
    elif args.pgd:
        attack = PGD(estimator=classifier, eps=float(run_args['eps']), eps_step=float(run_args['eps_step']), max_iter=int(run_args['max_iter']), verbose=False)
    elif args.deepfool:
        attack = DeepFool(classifier=classifier, max_iter=int(run_args['max_iter']), verbose=False)
    elif args.square:
        attack = Square(estimator=classifier, eps=float(run_args['eps']), max_iter=int(run_args['max_iter']), verbose=False)

    x_test_adv = attack.generate(x=x_test)

    predictions_adv = classifier.predict(x_test_adv)
    accuracy_adv = np.sum(np.argmax(predictions_adv, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)

    path = plot_samples(1, x_test, x_test_adv, y_test, predictions_adv)

    results = {
        "reg_acc": (accuracy) * 100,
        "adv_acc": (accuracy_adv) * 100,
        "figure": path
    }

    print(json.dumps(results))

    return results
if __name__ == "__main__":
    args, run_args = parse_args()
    run(args, run_args)
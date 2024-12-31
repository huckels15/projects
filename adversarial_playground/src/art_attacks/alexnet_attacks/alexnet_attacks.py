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
import os
import cv2
import json

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


IMG_HEIGHT, IMG_WIDTH = 32, 32
NUM_CLASSES = 43


def generator(dataset_path, batch_size):
    '''
    Generator to be space efficient when loading data for attacks.
    '''
    data = []
    for class_id in range(NUM_CLASSES):
        class_path = os.path.join(dataset_path, str(class_id))
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            data.append((img_path, class_id))
    
    np.random.shuffle(data)
    
    images, labels = [], []
    for img_path, class_id in data:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT)) 
        images.append(img / 255.0)
        labels.append(to_categorical(class_id, NUM_CLASSES))
        
        if len(images) == batch_size:
            yield np.array(images), np.array(labels)
            images, labels = [], []
    
    if images:
        yield np.array(images), np.array(labels)


def plot_samples(num_samples, x_test, x_test_adv, y_test, predictions_adv):
    '''
    Function to plot a sample before and after adversarial perturbations.
    '''
    class_map = {
        0: 'Speed limit (20km/h)',
        1: 'Speed limit (30km/h)',
        2: 'Speed limit (50km/h)',
        3: 'Speed limit (60km/h)',
        4: 'Speed limit (70km/h)',
        5: 'Speed limit (80km/h)',
        6: 'End of speed limit (80km/h)',
        7: 'Speed limit (100km/h)',
        8: 'Speed limit (120km/h)',
        9: 'No passing',
        10: 'No passing for vehicles over 3.5 metric tons',
        11: 'Right-of-way at the next intersection',
        12: 'Priority road',
        13: 'Yield',
        14: 'Stop',
        15: 'No vehicles',
        16: 'Vehicles over 3.5 metric tons prohibited',
        17: 'No entry',
        18: 'General caution',
        19: 'Dangerous curve to the left',
        20: 'Dangerous curve to the right',
        21: 'Double curve',
        22: 'Bumpy road',
        23: 'Slippery road',
        24: 'Road narrows on the right',
        25: 'Road work',
        26: 'Traffic signals',
        27: 'Pedestrians',
        28: 'Children crossing',
        29: 'Bicycles crossing',
        30: 'Beware of ice/snow',
        31: 'Wild animals crossing',
        32: 'End of all speed and passing limits',
        33: 'Turn right ahead',
        34: 'Turn left ahead',
        35: 'Ahead only',
        36: 'Go straight or right',
        37: 'Go straight or left',
        38: 'Keep right',
        39: 'Keep left',
        40: 'Roundabout mandatory',
        41: 'End of no passing',
        42: 'End of no passing by vehicles over 3.5 metric tons'
    }
    os.makedirs("figures", exist_ok=True)

    for i in range(num_samples):
        true_label = class_map[np.argmax(y_test[i])] 
        adv_pred_label = class_map[np.argmax(predictions_adv[i])]

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        ax[0].imshow((x_test[i] * 255).astype(np.uint8))
        ax[0].set_title(f"Original\nTrue: {true_label}", fontsize=12, color="green")
        ax[0].axis('off')

        ax[1].imshow((x_test_adv[i] * 255).astype(np.uint8))
        ax[1].set_title(f"Adversarial\nTrue: {true_label}\nPred: {adv_pred_label}", fontsize=12, color="red")
        ax[1].axis('off')

        fig.suptitle(f"Example {i + 1}", fontsize=14, fontweight="bold")
        plt.savefig(f"figures/example_{i + 1}_original_vs_adversarial.png")
        plt.close(fig)
    path = "figures/example_1_original_vs_adversarial.png"
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
    Function to run adversarial examaple attacks on alexnet model.
    '''
    train_path = "data/adversarial_testing"

    batch_size = 64
    train_generator = generator(train_path, batch_size)

    custom_objects = {"Adam": Adam}
    model = tf.keras.models.load_model("models/trainedAlexNet_20241118_1535.h5", custom_objects=custom_objects, compile=False)
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    min_pixel_value, max_pixel_value = 0.0, 1.0
    classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

    x_test, y_test = next(train_generator)
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
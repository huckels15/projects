import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.applications import ResNet101
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Input
import pandas as pd
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import ProjectedGradientDescent as PGD
from google.cloud import storage
import wandb
from wandb.integration.keras import WandbCallback
import argparse
import os

tf.compat.v1.disable_eager_execution()

def download_resnet_data(bucket_name, source_directory, destination_directory):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_directory)

    os.makedirs(destination_directory, exist_ok=True)

    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        
        file_name = os.path.basename(blob.name)
        destination_file_name = os.path.join(destination_directory, file_name)
        blob.download_to_filename(destination_file_name)

        print(f"Downloaded {blob.name}")

def load_data(local_csv_path):
    data = pd.read_csv(local_csv_path)
    y = data['label']
    X = data.drop(columns=['label'])

    X = X.values.reshape(-1, 28, 28, 3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    y_train = to_categorical(y_train, num_classes=7)
    y_val = to_categorical(y_val, num_classes=7)
    y_test = to_categorical(y_test, num_classes=7)

    with tf.compat.v1.Session() as sess:
        X_train = sess.run(tf.image.resize(X_train, (224, 224)))
        X_val = sess.run(tf.image.resize(X_val, (224, 224)))
        X_test = sess.run(tf.image.resize(X_test, (224, 224)))

    return X_train, y_train, X_val, y_val, X_test, y_test


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="pgd_at_resnet", help="Model name")
    parser.add_argument("--epochs", type=int, default=20, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--data_bucket", type=str, default="resnet-data-wf", help="GCS bucket for data")
    parser.add_argument("--data_path", type=str, default="data/hmnist_28_28_RGB.csv", help="Path to data in GCS bucket")
    parser.add_argument("--model_bucket", type=str, default="pgd-at-resnet-models-ac215", help="GCS bucket for saving model")
    parser.add_argument("--pretrained_model", type=str, default="gs://resnet-models-ac215/resnet.h5", help="Path to the pretrained ResNet model in GCS")
    parser.add_argument("--wandb_key", type=str, required=True, help="WandB API key")
    args = parser.parse_args()

    download_resnet_data(args.data_bucket, "data/", "resnet_data")

    wandb.login(key=args.wandb_key)
    wandb.init(
        project="blackknights_resnet",
        config={
            "architecture": "PGD AT ResNet101",
            "dataset": "HAM10000",
            "batch_size": args.batch_size,
            "epochs": args.epochs,
            "model_name": args.model_name,
        },
    )

    X_train, y_train, X_val, y_val, X_test, y_test = load_data("resnet_data/hmnist_28_28_RGB.csv")

    resnet = tf.keras.models.load_model(args.pretrained_model)
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=0.001)
    resnet.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    classifier = KerasClassifier(model=resnet, clip_values=(0.0, 1.0), use_logits=False)

    test_loss, test_accuracy = resnet.evaluate(X_test, y_test, verbose=0)
    print(f"Accuracy on benign test examples: {test_accuracy * 100:.2f}%")

    attack = PGD(estimator=classifier, eps=0.2, eps_step=0.01, max_iter=20, targeted=False)
    X_test_adv = attack.generate(x=X_test)

    predictions_adv = classifier.predict(X_test_adv)
    accuracy_adv = np.sum(np.argmax(predictions_adv, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
    print(f"Accuracy on adversarial examples before adv training: {accuracy_adv * 100:.2f}%")

    X_train_adv = attack.generate(x=X_train[:2000])

    es = EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)
    resnet.fit(
        X_train_adv,
        y_train[:2000],
        batch_size=args.batch_size,
        epochs=args.epochs,
        callbacks=[es, WandbCallback()],
    )

    loss, acc = resnet.evaluate(X_test_adv, y_test)
    print(f"Accuracy on adversarial examples after adv training: {acc * 100:.2f}%")

    local_model_path = f"{args.model_name}_pgd_at.h5"
    resnet.save(local_model_path)

    storage_client = storage.Client()
    bucket = storage_client.bucket(args.model_bucket)
    blob = bucket.blob(f"{args.model_name}_pgd_at.h5")
    blob.upload_from_filename(local_model_path)

    print(f"Model successfully uploaded to gs://{args.model_bucket}/{args.model_name}_pgd_at.h5")
    wandb.finish()

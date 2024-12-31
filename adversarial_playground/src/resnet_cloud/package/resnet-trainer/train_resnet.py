import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.applications import ResNet101
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Input
import pandas as pd
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import datetime
import matplotlib.pyplot as plt
import wandb
from wandb.integration.keras import WandbCallback
from google.cloud import storage
import argparse
import os

def get_resnet():
    resnet = ResNet101(weights='imagenet', include_top = False)
    resnet.trainable = False
    inputs = Input(shape=(224, 224, 3))
    x = resnet(inputs)
    x = Flatten()(x)
    x = Dense(128, activation = 'relu')(x)
    output = Dense(7, activation = 'softmax')(x)

    model = Model(inputs, output)
    model.summary()

    return model
    

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

def load_data():
    data = pd.read_csv("resnet_data/hmnist_28_28_RGB.csv")
    y = data['label']
    X = data.drop(columns= ['label'])

    X = X.values.reshape(-1, 28, 28, 3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)

    y_train = to_categorical(y_train, num_classes=7)
    y_val = to_categorical(y_val, num_classes=7)
    y_test = to_categorical(y_test, num_classes=7)

    X_train_resize = tf.image.resize(X_train, (224, 224))
    X_val_resize = tf.image.resize(X_val, (224, 224))
    X_test_resize = tf.image.resize(X_test, (224, 224))
    
    train_gen = train_datagen.flow(X_train_resize.numpy(), y_train, batch_size=args.batch_size)
    val_gen = test_datagen.flow(X_val_resize.numpy(), y_val, batch_size=args.batch_size)
    test_gen = test_datagen.flow(X_test_resize.numpy(), y_test, batch_size=args.batch_size)
    return train_gen, val_gen, test_gen

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_name", 
    dest="model_name", 
    default="resnet", 
    type=str, 
    help="Model name"
    )
parser.add_argument(
    "--epochs", 
    dest="epochs", 
    default=100, 
    type=int, 
    help="Number of epochs."
    )
parser.add_argument(
    "--batch_size", 
    dest="batch_size", 
    default=32, 
    type=int, 
    help="Size of a batch."
    )
parser.add_argument(
    "--model_bucket", 
    dest="model_bucket", 
    default="resnet-models-ac215", 
    type=str, 
    help="Bucket for models."
    )
parser.add_argument(
    "--data_bucket", 
    dest="data_bucket", 
    default="resnet-data-wf", 
    type=str, 
    help="Bucket for data."
    )
parser.add_argument(
    "--wandb_key",
    dest='wandb_key',
    default='16',
    type=str,
    help='WandB API Key'
)
args = parser.parse_args()

es = EarlyStopping(
    monitor="val_loss",
    min_delta=0.01,
    patience=10,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=True,
    start_from_epoch=0,
)

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)
test_datagen = tf.keras.preprocessing.image.ImageDataGenerator()

if __name__ == "__main__":
    dt = datetime.datetime.today()
    model_name = f"resnet"

    download_resnet_data(args.data_bucket, 'data/', 'resnet_data')
    wandb.login(key=args.wandb_key)
    wandb.init(
        project='blackknights_resnet', 
        config={
            'architecture': "ResNet101",
            'dataset': "HAM10000",
            'batch_size': args.batch_size,
            'epochs': args.epochs,
            'model_name': model_name
        }
    )

    resnet = get_resnet()
    train_gen, val_gen, test_gen = load_data()

    resnet.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = resnet.fit(train_gen, epochs=args.epochs, validation_data=val_gen, callbacks=[es, WandbCallback()])
    
    local_model_path = f"{model_name}.h5"
    resnet.save(local_model_path)

    gcs_model_path = f"{model_name}.h5"
    storage_client = storage.Client()
    bucket = storage_client.bucket(args.model_bucket)
    blob = bucket.blob(gcs_model_path)

    blob.upload_from_filename(local_model_path)

    print(f"Model successfully uploaded to gs://{args.model_bucket}/{gcs_model_path}")
    wandb.finish()
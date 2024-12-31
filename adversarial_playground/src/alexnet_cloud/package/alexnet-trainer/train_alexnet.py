import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import argparse
import wandb
from wandb.integration.keras import WandbCallback
from google.cloud import storage

strategy = tf.distribute.MirroredStrategy()
IMG_HEIGHT, IMG_WIDTH = 32, 32
NUM_CLASSES = 43
BATCH_SIZE = 32
EPOCHS = 100

def create_dataset(dataset_path, batch_size, shuffle=True):
    def parse_image(file_path):
        label = tf.strings.to_number(tf.strings.split(file_path, '/')[-2], out_type=tf.int32)
        img_bytes = tf.io.read_file(file_path)
        img = tf.image.decode_png(img_bytes, channels=3)
        img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
        img = img / 255.0 
        return img, tf.one_hot(label, NUM_CLASSES)

    dataset = tf.data.Dataset.list_files(f"{dataset_path}/*/*", shuffle=shuffle)
    dataset = dataset.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset

def create_alexnet():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(64, (3, 3), padding='same', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(512, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.Conv2D(512, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, default="gs://alexnet-data-multi/data/Train", help="Path to the dataset (local or GCS)")
    parser.add_argument("--epochs", type=int, default=EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--model_name", type=str, default="alexnet", help="Model name")
    parser.add_argument("--model_bucket", type=str, default="alexnet-models-ac215", help="Model save bucket")
    parser.add_argument("--wandb_project", type=str, default="alexnet_project", help="WandB project name")
    parser.add_argument("--wandb_key", type=str)
    args = parser.parse_args()

    train_ds = create_dataset(args.dataset_path, args.batch_size, shuffle=True)

    wandb.login(key=args.wandb_key)
    wandb.init(project=args.wandb_project, config={
        "architecture": "AlexNet",
        "batch_size": args.batch_size,
        "epochs": args.epochs
    })
    
    with strategy.scope():
        model = create_alexnet()
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    es = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
    history = model.fit(
        train_ds,
        epochs=args.epochs,
        callbacks=[es, WandbCallback()]
    )

    local_model_path = f"{args.model_name}.h5"
    model.save(local_model_path)

    gcs_model_path = f"{args.model_name}.h5"
    storage_client = storage.Client()
    bucket = storage_client.bucket(args.model_bucket)
    blob = bucket.blob(gcs_model_path)

    blob.upload_from_filename(local_model_path)

    print(f"Model successfully uploaded to gs://{args.model_bucket}/{gcs_model_path}")
    wandb.finish()

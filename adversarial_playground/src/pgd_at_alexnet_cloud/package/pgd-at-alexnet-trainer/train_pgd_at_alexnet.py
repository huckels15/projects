import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from google.cloud import storage
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import ProjectedGradientDescent as PGD
import wandb
from wandb.integration.keras import WandbCallback
import argparse

tf.compat.v1.disable_eager_execution()

IMG_HEIGHT, IMG_WIDTH = 32, 32
NUM_CLASSES = 43
BATCH_SIZE = 32
EPOCHS = 20

def create_dataset(dataset_path, batch_size, shuffle=True):
    def parse_image(file_path):
        label = tf.strings.to_number(tf.strings.split(file_path, '/')[-2], out_type=tf.int32)
        img_bytes = tf.io.read_file(file_path)
        img = tf.image.decode_png(img_bytes, channels=3)
        img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
        img = img / 255.0  # Normalize pixel values to [0, 1]
        return img, tf.one_hot(label, NUM_CLASSES)

    dataset = tf.data.Dataset.list_files(f"{dataset_path}/*/*", shuffle=shuffle)
    dataset = dataset.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, default="gs://alexnet-data-multi/data/Train", help="Path to the dataset (local or GCS)")
    parser.add_argument("--pretrained_model", type=str, default="gs://alexnet-models-ac215/alexnet.h5", help="Path to the pretrained AlexNet model in GCS")
    parser.add_argument("--epochs", type=int, default=EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--model_name", type=str, default="alexnet", help="Model name")
    parser.add_argument("--model_bucket", type=str, default="pgd-at-alexnet-models-ac215", help="Model save bucket")
    parser.add_argument("--wandb_project", type=str, default="pgd_at_alexnet_project", help="WandB project name")
    parser.add_argument("--wandb_key", type=str)
    args = parser.parse_args()

    train_ds = create_dataset(args.dataset_path, args.batch_size, shuffle=True)

    wandb.login(key=args.wandb_key)
    wandb.init(project=args.wandb_project, config={
        "architecture": "PGD AT AlexNet",
        "batch_size": args.batch_size,
        "epochs": args.epochs
    })

    model = tf.keras.models.load_model(args.pretrained_model)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    iterator = tf.compat.v1.data.make_initializable_iterator(train_ds)
    next_element = iterator.get_next()

    with tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())

        classifier = KerasClassifier(model=model, clip_values=(0.0, 1.0), use_logits=False)
        attack = PGD(estimator=classifier, eps=0.2, eps_step=0.01, max_iter=20, targeted=False)

        for epoch in range(EPOCHS):
            print(f"Starting epoch {epoch + 1}/{EPOCHS}")

            sess.run(iterator.initializer)

            while True:
                try:
                    images, labels = sess.run(next_element)
                    
                    x_adv_batch = attack.generate(x=images)
                    
                    model.train_on_batch(x_adv_batch, labels)
                except tf.errors.OutOfRangeError:
                    break

        local_model_path = f"{args.model_name}_pgd_at.h5"
        model.save(local_model_path)

        gcs_model_path = f"{args.model_name}_pgd_at.h5"
        storage_client = storage.Client()
        bucket = storage_client.bucket(args.model_bucket)
        blob = bucket.blob(gcs_model_path)
        blob.upload_from_filename(local_model_path)

    print(f"Model successfully uploaded to gs://{args.model_bucket}/{gcs_model_path}")
    wandb.finish()

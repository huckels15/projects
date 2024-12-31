# Lint as: python3
"""Training for the visual wakewords person detection model.

The visual wakewords person detection model is a core model for the TinyMLPerf
benchmark suite. This script provides source for how the reference model was
created and trained, and can be used as a starting point for open submissions
using re-training.
"""

import os

from absl import app
from src.robustness_testing_pipeline.training.mobilenet.vww_model_logits import mobilenet_v1

import tensorflow as tf
from tensorflow.keras.losses import CategoricalCrossentropy
assert tf.__version__.startswith('2')
import datetime

# get date ant time to save model
dt = datetime.datetime.today()
year = dt.year
month = dt.month
day = dt.day
hour = dt.hour
minute = dt.minute

IMAGE_SIZE = 96
BATCH_SIZE = 32
EPOCHS = 20

BASE_DIR = os.path.join(os.getcwd(), '../Datasets/vw_coco2014_96')


def main(argv):
  if len(argv) >= 2:
    model = tf.keras.models.load_model(argv[1])
  else:
    model = mobilenet_v1()

  model.summary()

  batch_size = 50
  validation_split = 0.1

  datagen = tf.keras.preprocessing.image.ImageDataGenerator(
      rotation_range=10,
      width_shift_range=0.05,
      height_shift_range=0.05,
      zoom_range=.1,
      horizontal_flip=True,
      validation_split=validation_split,
      rescale=1. / 255)
  train_generator = datagen.flow_from_directory(
      BASE_DIR,
      target_size=(IMAGE_SIZE, IMAGE_SIZE),
      batch_size=BATCH_SIZE,
      subset='training',
      color_mode='rgb')
  val_generator = datagen.flow_from_directory(
      BASE_DIR,
      target_size=(IMAGE_SIZE, IMAGE_SIZE),
      batch_size=BATCH_SIZE,
      subset='validation',
      color_mode='rgb')
  print(train_generator.class_indices)

  model = train_epochs(model, train_generator, val_generator, 20, 0.001)
  model = train_epochs(model, train_generator, val_generator, 10, 0.0005)
  model = train_epochs(model, train_generator, val_generator, 20, 0.00025)

  # Save model HDF5
  if len(argv) >= 3:
    model.save(argv[2])
  else:
    model_name = f'vww_96_testable_logits.h5'
    model.save(f'models/' + model_name)


def train_epochs(model, train_generator, val_generator, epoch_count,
                 learning_rate):
  loss_func = CategoricalCrossentropy(from_logits=True)
  model.compile(
      optimizer=tf.keras.optimizers.Adam(learning_rate),
      loss=loss_func,
      metrics=['accuracy'])
  history_fine = model.fit(
      train_generator,
      steps_per_epoch=len(train_generator),
      epochs=epoch_count,
      validation_data=val_generator,
      validation_steps=len(val_generator),
      batch_size=BATCH_SIZE)
  return model


if __name__ == '__main__':
  app.run(main)

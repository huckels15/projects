import os
import pickle
import numpy as np
import tensorflow as tf
import math


def get_cifar10_test_ds_f32(negatives=False):
    data_dir = os.path.join(os.path.dirname(__file__), '../src/robustness_testing_pipeline/Datasets/cifar-10-batches-py')

    cifar_test_data_dict = unpickle(data_dir + "/test_batch")
    cifar_test_data = cifar_test_data_dict[b'data']
    cifar_test_labels = cifar_test_data_dict[b'labels']

    cifar_test_data = cifar_test_data.reshape((len(cifar_test_data), 3, 32, 32))
    if negatives:
        cifar_test_data = cifar_test_data.transpose(0, 2, 3, 1).astype(np.float32)
    else:
        cifar_test_data = np.rollaxis(cifar_test_data, 1, 4)
    cifar_test_labels = np.array(cifar_test_labels)

    cifar_test_data = np.array(cifar_test_data / 255).astype(np.float32)
    cifar_test_labels = tf.one_hot(cifar_test_labels, 10).numpy()

    return cifar_test_data, cifar_test_labels


def get_cifar10_train_ds_f32(negatives=False):
    data_dir = os.path.join(os.path.dirname(__file__), '../src/robustness_testing_pipeline/Datasets/cifar-10-batches-py')

    # Load all training batches
    cifar_train_data = []
    cifar_train_labels = []
    for i in range(1, 6):
        data_batch_dict = unpickle(os.path.join(data_dir, f"data_batch_{i}"))
        cifar_train_data.append(data_batch_dict[b'data'])
        cifar_train_labels += data_batch_dict[b'labels']

    # Concatenate all training batches
    cifar_train_data = np.vstack(cifar_train_data)
    cifar_train_labels = np.array(cifar_train_labels)

    # Reshape and process data
    cifar_train_data = cifar_train_data.reshape((len(cifar_train_data), 3, 32, 32))
    if negatives:
        cifar_train_data = cifar_train_data.transpose(0, 2, 3, 1).astype(np.float32)
    else:
        cifar_train_data = np.rollaxis(cifar_train_data, 1, 4)
    
    # Normalize data to range [0, 1]
    cifar_train_data = np.array(cifar_train_data / 255).astype(np.float32)
    
    # One-hot encode the labels
    cifar_train_labels = tf.one_hot(cifar_train_labels, 10).numpy()

    return cifar_train_data, cifar_train_labels

def unpickle(file):
    """load the cifar-10 data"""

    with open(file, 'rb') as fo:
        data = pickle.load(fo, encoding='bytes')
    return data


def get_vww_test_ds_f32():
    data_test = []
    labels_test = []
    data_dir = os.path.join(os.path.dirname(__file__), '../src/robustness_testing_pipeline/Datasets/vw_coco2014_96')

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=.1,
        horizontal_flip=True,
        validation_split=0.1,
        rescale=1. / 255)
    val_generator = datagen.flow_from_directory(
        data_dir,
        target_size=(96, 96),
        batch_size=1,
        subset='validation',
        color_mode='rgb',
        shuffle=False)

    batch_index = 0
    while batch_index < val_generator.n:
        data = next(val_generator) # changed this
        data_test.append(data[0][0])
        labels_test.append(np.argmax(data[1][0]))
        batch_index = batch_index + 1

    data_test = np.array(data_test)
    labels_test = tf.one_hot(labels_test, 2).numpy()

    return data_test, labels_test

def get_vww_train_ds_f32(batch_limit=625, batch_size=32):
    data_train = []
    labels_train = []
    data_dir = os.path.join(os.path.dirname(__file__), '../src/robustness_testing_pipeline/Datasets/vw_coco2014_96')
    
    # Calculate number of batches needed per class
    samples_per_class = (batch_limit * batch_size) // 2  # 10000 per class for batch_limit=625 and batch_size=32
    batches_per_class = math.ceil(samples_per_class / batch_size)  # Number of batches per class

    # ImageDataGenerator for training data
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=0.1,
        horizontal_flip=True,
        rescale=1. / 255
    )

    # Generators for each class
    class_dirs = ['person', 'non_person']
    for i, class_dir in enumerate(class_dirs):
        class_generator = datagen.flow_from_directory(
            data_dir,
            target_size=(96, 96),
            batch_size=batch_size,
            classes=[class_dir],
            color_mode='rgb',
            shuffle=True
        )

        # Collect the required number of batches from each class
        for _ in range(batches_per_class):
            data = next(class_generator)  # Get a batch of images and labels
            data_train.extend(data[0])  # Append all images in the batch
            labels_train.extend(np.argmax(data[1], axis=1))  # Append the corresponding labels

    # Convert lists to arrays and one-hot encode labels
    data_train = np.array(data_train)
    labels_train = tf.one_hot(labels_train, 2).numpy()

    # Shuffle dataset to mix classes
    indices = np.arange(data_train.shape[0])
    np.random.shuffle(indices)
    data_train, labels_train = data_train[indices], labels_train[indices]

    return data_train, labels_train


# def get_vww_train_ds_f32(batch_limit=625, batch_size=32):
#     data_train = []
#     labels_train = []
#     data_dir = os.path.join(os.path.dirname(__file__), '../../Datasets/vw_coco2014_96')
    
#     # Calculate number of batches needed per class
#     samples_per_class = (batch_limit * batch_size) // 2  # 10000 per class for batch_limit=625 and batch_size=32
#     batches_per_class = math.ceil(samples_per_class / batch_size)  # Number of batches per class

#     # ImageDataGenerator for training data
#     datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#         rotation_range=10,
#         width_shift_range=0.05,
#         height_shift_range=0.05,
#         zoom_range=0.1,
#         horizontal_flip=True,
#         rescale=1. / 255
#     )

#     # Generators for each class
#     class_dirs = ['person', 'non_person']
#     for i, class_dir in enumerate(class_dirs):
#         class_generator = datagen.flow_from_directory(
#             data_dir,
#             target_size=(96, 96),
#             batch_size=batch_size,
#             classes=[class_dir],
#             color_mode='rgb',
#             shuffle=True
#         )

#         # Collect the required number of batches from each class
#         for _ in range(batches_per_class):
#             data = next(class_generator)  # Get a batch of images and labels
#             data_train.extend(data[0])  # Append all images in the batch
#             labels_train.extend([i] * batch_size)  # Append the corresponding labels for each image

#     # Convert lists to arrays and one-hot encode labels
#     data_train = np.array(data_train)
#     labels_train = tf.one_hot(labels_train, 2).numpy()

#     # Shuffle dataset to mix classes
#     indices = np.arange(data_train.shape[0])
#     np.random.shuffle(indices)
#     data_train, labels_train = data_train[indices], labels_train[indices]

#     return data_train, labels_train

# def get_vww_train_ds_f32(batch_limit=625):  # Add a batch_limit parameter
#     data_train = []
#     labels_train = []
#     data_dir = os.path.join(os.path.dirname(__file__), '../../Datasets/vw_coco2014_96')

#     # ImageDataGenerator for training data
#     datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#         rotation_range=10,
#         width_shift_range=0.05,
#         height_shift_range=0.05,
#         zoom_range=.1,
#         horizontal_flip=True,
#         validation_split=0.1,  # Use this only if part of the data is for validation
#         rescale=1. / 255
#     )

#     # Generate training data from the training subset
#     train_generator = datagen.flow_from_directory(
#         data_dir,
#         target_size=(96, 96),
#         batch_size=32,
#         subset='training',  # Use the 'training' subset
#         color_mode='rgb',
#         shuffle=False
#     )

#     batch_index = 0
#     # Loop through the batches, stopping early once the batch_limit is reached
#     while batch_index < batch_limit and batch_index < train_generator.n:
#         data = next(train_generator)  # Get the next batch of images and labels
#         data_train.append(data[0][0])  # Append image data
#         labels_train.append(np.argmax(data[1][0]))  # Append the label (one-hot to class index)
#         batch_index += 1

#     data_train = np.array(data_train)
#     labels_train = tf.one_hot(labels_train, 2).numpy()  # One-hot encode the labels

#     return data_train, labels_train
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Activation, BatchNormalization, ZeroPadding2D, Dropout
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.regularizers import l2
from src.robustness_testing_pipeline.training.mobilenet.vww_model import mobilenet_v1
from src.robustness_testing_pipeline.training.mobilenet.vww_model_logits import mobilenet_v1_logits

#keras deep-cv


def create_basic():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))  # Added another dense layer for a better balance
    model.add(Dense(10, activation='softmax'))
    return model

def create_lenet():

	# Initialize model
	lenet = Sequential()

	# 2 sets of CRP (Convolution, RELU, Pooling)
	lenet.add(Conv2D(32, (5, 5), padding="same",
		input_shape=(32, 32, 3), kernel_regularizer=l2(0.)))
	lenet.add(Activation("relu"))
	lenet.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

	lenet.add(Conv2D(32, (5, 5), padding="same",
		kernel_regularizer=l2(0.)))
	lenet.add(Activation("relu"))
	lenet.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

	# Fully connected layers (w/ RELU)
	lenet.add(Flatten())
	lenet.add(Dense(500, kernel_regularizer=l2(0.)))
	lenet.add(Activation("relu"))

	# Softmax (for classification)
	lenet.add(Dense(10, kernel_regularizer=l2(0.)))
	lenet.add(Activation("softmax"))

	# Return the constructed network
	return lenet

def create_alexnet():
    alexnet = Sequential()

    # Layer 1: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(64, (3, 3), input_shape=(32, 32, 3), padding='same', kernel_regularizer=l2(0.0005)))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 2: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(128, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 3: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(256, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 4: Conv -> ReLU
    alexnet.add(Conv2D(512, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))

    # Layer 5: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(512, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Fully connected layers
    alexnet.add(Flatten())
    alexnet.add(Dense(512, activation='relu'))
    alexnet.add(Dropout(0.5))

    alexnet.add(Dense(512, activation='relu'))
    alexnet.add(Dropout(0.5))

    # Output layer
    alexnet.add(Dense(10, activation='softmax'))

    return alexnet


def create_resnet():

    input_shape=[32,32,3]
    num_classes=10
    num_filters = 16

    inputs = Input(shape=input_shape)
    x = Conv2D(num_filters,
                  kernel_size=3,
                  strides=1,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    y = Conv2D(num_filters,
                  kernel_size=3,
                  strides=1,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(x)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Conv2D(num_filters,
                  kernel_size=3,
                  strides=1,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(y)
    y = BatchNormalization()(y)

    x = tf.keras.layers.add([x, y])
    x = Activation('relu')(x)

    num_filters = 32 
    y = Conv2D(num_filters,
                  kernel_size=3,
                  strides=2,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(x)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Conv2D(num_filters,
                  kernel_size=3,
                  strides=1,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(y)
    y = BatchNormalization()(y)

    x = Conv2D(num_filters,
                  kernel_size=1,
                  strides=2,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(x)

    x = tf.keras.layers.add([x, y])
    x = Activation('relu')(x)

    num_filters = 64
    y = Conv2D(num_filters,
                  kernel_size=3,
                  strides=2,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(x)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Conv2D(num_filters,
                  kernel_size=3,
                  strides=1,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(y)
    y = BatchNormalization()(y)

    x = Conv2D(num_filters,
                  kernel_size=1,
                  strides=2,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=l2(1e-4))(x)

    x = tf.keras.layers.add([x, y])
    x = Activation('relu')(x)

    pool_size = int(np.amin(x.shape[1:3]))
    x = AveragePooling2D(pool_size=pool_size)(x)
    y = Flatten()(x)
    outputs = Dense(num_classes,
                    activation='softmax',
                    kernel_initializer='he_normal')(y)

    # Instantiate model.
    model = Model(inputs=inputs, outputs=outputs)
    return model

def create_basic_logits():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))  # Added another dense layer for a better balance
    model.add(Dense(10, activation='linear'))

    return model

def create_lenet_logits():

	# Initialize model
	lenet = Sequential()

	# 2 sets of CRP (Convolution, RELU, Pooling)
	lenet.add(Conv2D(32, (5, 5), padding="same",
		input_shape=(32, 32, 3), kernel_regularizer=l2(0.)))
	lenet.add(Activation("relu"))
	lenet.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

	lenet.add(Conv2D(32, (5, 5), padding="same",
		kernel_regularizer=l2(0.)))
	lenet.add(Activation("relu"))
	lenet.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

	# Fully connected layers (w/ RELU)
	lenet.add(Flatten())
	lenet.add(Dense(500, kernel_regularizer=l2(0.)))
	lenet.add(Activation("relu"))

	# Softmax (for classification)
	lenet.add(Dense(10, kernel_regularizer=l2(0.)))

	# Return the constructed network
	return lenet

def create_alexnet_logits():
    alexnet = Sequential()

    # Layer 1: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(64, (3, 3), input_shape=(32, 32, 3), padding='same', kernel_regularizer=l2(0.0005)))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 2: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(128, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 3: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(256, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 4: Conv -> ReLU
    alexnet.add(Conv2D(512, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))

    # Layer 5: Conv -> ReLU -> MaxPool
    alexnet.add(Conv2D(512, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    # Fully connected layers
    alexnet.add(Flatten())
    alexnet.add(Dense(512, activation='relu'))
    alexnet.add(Dropout(0.5))

    alexnet.add(Dense(512, activation='relu'))
    alexnet.add(Dropout(0.5))

    # Output layer
    alexnet.add(Dense(10, activation='linear'))

    return alexnet


def create_resnet_logits():
    input_shape=[32,32,3]
    num_classes=10
    num_filters = 16

    inputs = Input(shape=input_shape)
    x = Conv2D(num_filters, kernel_size=3, strides=1, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    y = Conv2D(num_filters, kernel_size=3, strides=1, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(x)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Conv2D(num_filters, kernel_size=3, strides=1, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(y)
    y = BatchNormalization()(y)

    x = tf.keras.layers.add([x, y])
    x = Activation('relu')(x)

    num_filters = 32
    y = Conv2D(num_filters, kernel_size=3, strides=2, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(x)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Conv2D(num_filters, kernel_size=3, strides=1, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(y)
    y = BatchNormalization()(y)

    x = Conv2D(num_filters, kernel_size=1, strides=2, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(x)

    x = tf.keras.layers.add([x, y])
    x = Activation('relu')(x)

    num_filters = 64
    y = Conv2D(num_filters, kernel_size=3, strides=2, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(x)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Conv2D(num_filters, kernel_size=3, strides=1, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(y)
    y = BatchNormalization()(y)

    x = Conv2D(num_filters, kernel_size=1, strides=2, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(1e-4))(x)

    x = tf.keras.layers.add([x, y])
    x = Activation('relu')(x)

    pool_size = int(np.amin(x.shape[1:3]))
    x = AveragePooling2D(pool_size=pool_size)(x)
    y = Flatten()(x)
    outputs = Dense(num_classes, kernel_initializer='he_normal')(y)  # No activation for logits

    model = Model(inputs=inputs, outputs=outputs)
    return model

def create_mobilenet():
    return mobilenet_v1()

def create_mobilenet_logits():
    return mobilenet_v1_logits()
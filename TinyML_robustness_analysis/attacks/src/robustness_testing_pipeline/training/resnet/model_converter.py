'''
MLCommons
group: TinyMLPerf (https://github.com/mlcommons/tiny)

image classification on cifar10

model_converter.py desc: converts floating point model to fully int8
'''

import tensorflow as tf
import numpy as np
from src.robustness_testing_pipeline.training.resnet import train_resnet

cifar_10_dir = 'src/robustness_testing_pipeline/Datasets/cifar-10-batches-py'

def representative_dataset_generator():
    train_data, train_filenames, train_labels, test_data, test_filenames, test_labels, label_names = \
        train_resnet.load_cifar_10_data(cifar_10_dir)
    _idx = np.load('src/robustness_testing_pipeline/training/resnet/calibration_samples_idxs.npy')
    for i in _idx:
        sample_img = np.expand_dims(np.array(test_data[i], dtype=np.float32), axis=0)
        yield [sample_img]

def convert_model(model_name):
    tfmodel_path = 'src/robustness_testing_pipeline/models/fp_models/' + model_name
    tfmodel = tf.keras.models.load_model(tfmodel_path)
    model_name = model_name[:-3]
    converter = tf.lite.TFLiteConverter.from_keras_model(tfmodel)
    tflite_model = converter.convert()
    open('src/robustness_testing_pipeline/models/tflite_models/' + model_name + '.tflite', 'wb').write(tflite_model)

    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.representative_dataset = representative_dataset_generator
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
    tflite_quant_model = converter.convert()
    open('src/robustness_testing_pipeline/models/quant_models/' + model_name + '_quant.tflite', 'wb').write(tflite_quant_model)

import os

from absl import app

import tensorflow as tf
assert tf.__version__.startswith('2')

BASE_DIR = os.path.join(os.getcwd(), "src/robustness_testing_pipeline/Datasets/vw_coco2014_96")

def main(argv):
    if len(argv) != 2:
        raise app.UsageError('Usage: convert_vww.py <model_to_convert.h5>')
    model = tf.keras.models.load_model("src/robustness_testing_pipeline/models/fp_models/" + argv[1])
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with tf.io.gfile.GFile('src/robustness_testing_pipeline/models/tflite_models' + argv[1][:-3] + "_float.tflite", 'wb') as float_file:
        float_file.write(tflite_model)

    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    def representative_dataset_gen():
        dataset_dir = os.path.join(BASE_DIR, "person")
        for idx, image_file in enumerate(os.listdir(dataset_dir)):
            # 10 representative images should be enough for calibration.
            if idx > 10:
                return
            full_path = os.path.join(dataset_dir, image_file)
            if os.path.isfile(full_path):
                img = tf.keras.preprocessing.image.load_img(
                    full_path, color_mode='rgb').resize((96, 96))
                arr = tf.keras.preprocessing.image.img_to_array(img)
                # Scale input to [0, 1.0] like in training.
                yield [arr.reshape(1, 96, 96, 3) / 255.]

    # Convert model to full-int8 and save as quantized tflite flatbuffer.
    converter.representative_dataset = representative_dataset_gen
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
    quantized_tflite_model = converter.convert()
    with tf.io.gfile.GFile('src/robustness_testing_pipeline/models/quant_models' + argv[1][:-3] + '_quant.tflite', 'wb') as quantized_file:
        quantized_file.write(quantized_tflite_model)


def run_conversion(model_path):
    main([None, model_path])

if __name__ == '__main__':
    app.run(main)

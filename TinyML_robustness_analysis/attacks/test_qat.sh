DATASET_ID=cifar10
BASIC=basic
LENET=lenet
ALEXNET=alexnet
RESNET=resnet
DATASET_SIZE=1000
NUM_CLASSES=10
NB_EPOCS=80
NB_STOLEN=50000

QNN_INT8='src/robustness_testing_pipeline/models/target_models/trainedResnet_testable_quant.tflite'

python3 copycat_int8.py --dataset_id "$DATASET_ID" --qat --num_classes "$NUM_CLASSES" --nb_epochs "$NB_EPOCS" --nb_stolen "$NB_STOLEN" --target_int8 "$QNN_INT8" --theived_template "$ALEXNET"
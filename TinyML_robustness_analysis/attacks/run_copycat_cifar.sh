#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <nb_epochs> <nb_stolen>"
    exit 1
fi

NB_EPOCS=$1
NB_STOLEN=$2


DATASET_ID=cifar10
BASIC=basic
LENET=lenet
ALEXNET=alexnet
RESNET=resnet
DATASET_SIZE=1000
NUM_CLASSES=10

QNN_INT8='src/robustness_testing_pipeline/models/target_models/trainedResnet_testable_quant.tflite'

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_PREFIX="knockoff_vww_results_${TIMESTAMP}"

echo "=============================================================="
echo "======================CopycatCNN -- Basic  =============================="
echo "Basic Arch Results:" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
python3 copycat_int8.py --dataset_id "$DATASET_ID" --num_classes "$NUM_CLASSES" --nb_epochs "$NB_EPOCS" --nb_stolen "$NB_STOLEN" --target_int8 "$QNN_INT8" --theived_template "$BASIC" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
echo "" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"

echo "=============================================================="
echo "======================CopycatCNN -- Lenet  =============================="
echo "Lenet Arch Results:" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
python3 copycat_int8.py --dataset_id "$DATASET_ID" --num_classes "$NUM_CLASSES" --nb_epochs "$NB_EPOCS" --nb_stolen "$NB_STOLEN" --target_int8 "$QNN_INT8" --theived_template "$LENET" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
echo "" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"

echo "=============================================================="
echo "======================CopycatCNN -- Alexnet  =============================="
echo "Alexnet Arch Results:" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
python3 copycat_int8.py --dataset_id "$DATASET_ID" --num_classes "$NUM_CLASSES" --nb_epochs "$NB_EPOCS" --nb_stolen "$NB_STOLEN" --target_int8 "$QNN_INT8" --theived_template "$ALEXNET" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
echo "" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"

echo "=============================================================="
echo "======================CopycatCNN -- Resnet  =============================="
echo "Resnet Arch Results:" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
python3 copycat_int8.py --dataset_id "$DATASET_ID" --num_classes "$NUM_CLASSES" --nb_epochs "$NB_EPOCS" --nb_stolen "$NB_STOLEN" --target_int8 "$QNN_INT8" --theived_template "$RESNET" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"
echo "" >> "${OUTPUT_PREFIX}_${NB_STOLEN}_${NB_EPOCS}.txt"



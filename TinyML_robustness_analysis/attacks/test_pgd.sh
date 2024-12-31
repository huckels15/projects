#!/bin/bash
DATASET_ID=cifar10
DATASET_SIZE=1000
NUM_CLASSES=10
ANN_FLOAT='src/robustness_testing_pipeline/models/qat_models/stolen_alexnet_cifar_20241125_2203_qat_test.h5'

python3 test_pgd.py --dataset_id "$DATASET_ID" --dataset_size "$DATASET_SIZE" --num_classes "$NUM_CLASSES" --ann_float "$ANN_FLOAT"  \
                --pgd_num_random_init 1 --pgd_max_iter 10 \
                --pgd_eps "0.1"

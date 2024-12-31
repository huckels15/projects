#!/bin/bash
set -e

mkdir -p /app/models

gsutil cp gs://pgd-at-resnet-models-ac215/trainedResnet_20241016_2112_pgd_robust.h5 /app/models/trainedResnet_20241016_2112_pgd_robust.h5
echo "Downloaded Resnet model weights"

uvicorn app:app --host 0.0.0.0 --port 8000
#!/bin/bash
set -e

mkdir -p /app/models

gsutil cp gs://resnet-models-ac215/trainedResnet_20241016_2143.h5 /app/models/trainedResnet_20241016_2143.h5
echo "Downloaded Resnet model weights"

uvicorn app:app --host 0.0.0.0 --port 8000
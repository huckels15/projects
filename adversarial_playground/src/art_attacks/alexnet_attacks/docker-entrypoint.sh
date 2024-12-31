#!/bin/bash
set -e

mkdir -p /app/models

# echo "Container is running!!!"
gsutil -m cp -r gs://alexnet-data-multi/adversarial_testing /app/data
echo "Downloaded data"

gsutil cp gs://alexnet-models-ac215/trainedAlexNet_20241118_1535.h5 /app/models/trainedAlexNet_20241118_1535.h5
echo "Downloaded AlexNet model weights"

uvicorn app:app --host 0.0.0.0 --port 8000
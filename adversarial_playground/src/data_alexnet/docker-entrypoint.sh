#!/bin/bash

echo "Container is running!!!"
# Ensure Kaggle credentials are set up
mkdir -p ~/.kaggle
cp /secrets/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Authenticate gcloud using service account
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
# Set GCP Project Details
gcloud config set project $GCP_PROJECT

python3 downloader.py



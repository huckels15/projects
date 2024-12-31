#!/bin/bash

export GCS_BUCKET_NAME="custom-attacks-multi"

set -e

# echo "Container is running!!!"

# mkdir -p /mnt/gcs_data
# gcsfuse --implicit-dirs $GCS_BUCKET_NAME /mnt/gcs_data
# echo "GCS bucket mounted at /mnt/gcs_data"

# mkdir -p /mnt/gcs_data/data
# mkdir -p /app/data
# mount --bind /mnt/gcs_data/data /app/data
# echo "Mounted /mnt/gcs_data/data to /app/data"

mkdir -p /mnt/gcs_bucket
gcsfuse --implicit-dirs  $GCS_BUCKET_NAME /mnt/gcs_data


uvicorn app:app --host 0.0.0.0 --port 8000

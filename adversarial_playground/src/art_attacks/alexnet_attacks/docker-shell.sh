#!/bin/bash

set -e

BUILD="True" 

export IMAGE_NAME="alexnet_attacks_vertex_ai"
export BASE_DIR=$(pwd)
export GCS_BUCKET_NAME="alexnet-data-multi"
export GCP_PROJECT="secret-cipher-399620"
export GCP_ZONE="us-east1"

if [ "$BUILD" == "True" ]; then 
    echo "Building image..."
    docker build -t $IMAGE_NAME -f Dockerfile .

    docker run --rm --name $IMAGE_NAME -ti \
        --privileged \
        --cap-add SYS_ADMIN \
        --device /dev/fuse \
        --mount type=bind,source="$BASE_DIR",target=/app \
        -e GCP_PROJECT=$GCP_PROJECT \
        -e GCP_ZONE=$GCP_ZONE \
        -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
        -p 8000:8000 \
        $IMAGE_NAME
    fi

if [ "$BUILD" != "True" ]; then 
    echo "Using prebuilt image..."
    docker run --rm --name $IMAGE_NAME -ti \
        --privileged \
        --cap-add SYS_ADMIN \
        --device /dev/fuse \
        --mount type=bind,source="$BASE_DIR",target=/app \
        -e GCP_PROJECT=$GCP_PROJECT \
        -e GCP_ZONE=$GCP_ZONE \
        -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
        -p 8000:8000 \
        $IMAGE_NAME
fi
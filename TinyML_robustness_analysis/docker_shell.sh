#!/bin/bash

set -e

BUILD="False" 

export IMAGE_NAME="tinyml_robustness"
export BASE_DIR=$(pwd)

if [ "$BUILD" == "True" ]; then 
    echo "Building image..."
    docker build -t $IMAGE_NAME -f Dockerfile .

    # Run the container
    docker run --gpus=all --rm --name $IMAGE_NAME -ti \
    --mount type=bind,source="$BASE_DIR",target=/app $IMAGE_NAME
fi

if [ "$BUILD" != "True" ]; then 
    echo "Using prebuilt image..."
    # Run the container
    docker run --gpus=all --rm --name $IMAGE_NAME -ti \
    --mount type=bind,source="$BASE_DIR",target=/app $IMAGE_NAME
fi
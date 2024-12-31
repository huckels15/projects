#!/bin/bash

set -e  # Exit immediately on error
set -x  # Debug: Print each command

# Configuration
BUILD="False"  # Set to "True" to build the image, "False" to use a prebuilt image
export IMAGE_NAME="frontend-dev"  # Unified container name to match the Dockerfile
export BASE_DIR=$(pwd)
export GCP_PROJECT="secret-cipher-399620"
export GCP_ZONE="us-east1"
export FRONTEND_PORT=3000
export BACKEND_PORT=3001

# Function to build the Docker image
build_image() {
    echo "Building Docker image: $IMAGE_NAME"
    docker build -t "$IMAGE_NAME" -f Dockerfile.test .
}

# Function to run the Docker container
run_container() {
    echo "Running Docker container: $IMAGE_NAME"

    docker run --rm --name "$IMAGE_NAME" -ti \
        --privileged \
        --cap-add SYS_ADMIN \
        --device /dev/fuse \
        --mount type=bind,source="$BASE_DIR/frontend",target=/app/frontend,consistency=delegated \
        --mount type=bind,source="$BASE_DIR/backend",target=/app/backend,consistency=delegated \
        -e GCP_PROJECT="$GCP_PROJECT" \
        -e GCP_ZONE="$GCP_ZONE" \
        -p "$FRONTEND_PORT:3000" \
        -p "$BACKEND_PORT:3001" \
        "$IMAGE_NAME"
}

# Main script logic
echo "Select an option:"
echo "1. Build and Run Container"
echo "2. Run Container (Use Prebuilt Image)"
read -p "Enter your choice: " CHOICE

case $CHOICE in
    1)
        BUILD="True"
        build_image
        run_container
        ;;
    2)
        run_container
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

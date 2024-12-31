#!/bin/bash

# Define the image name
IMAGE_NAME="frontend"

# Build the Docker image
echo "Building the Docker image..."
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the Docker container with the appropriate configurations
echo "Running the Docker container..."
docker run --rm --name $IMAGE_NAME -ti \
  -v "$(pwd):/app" \
  -p 3000:3000 \
  -p 3001:3001 \
  $IMAGE_NAME


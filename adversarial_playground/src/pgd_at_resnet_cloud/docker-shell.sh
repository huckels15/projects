export IMAGE_NAME=resnet-training-cli
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCS_BUCKET_URI="gs://pgd-at-resnet-trainer"
export GCP_PROJECT="secret-cipher-399620"


BUILD="True" 

if [ "$BUILD" == "True" ]; then 
    # Build the image based on the Dockerfile
    docker build -t $IMAGE_NAME -f Dockerfile .

    # Run Container
    docker run --rm --name $IMAGE_NAME -ti \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-trainer-two.json \
    -e GCP_PROJECT=$GCP_PROJECT \
    -e GCS_BUCKET_URI=$GCS_BUCKET_URI \
    -e WANDB_KEY=$WANDB_KEY \
    $IMAGE_NAME
fi

if [ "$BUILD" != "True" ]; then 
    # Run Container
    docker run --rm --name $IMAGE_NAME -ti \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/model-trainer.json \
    -e GCP_PROJECT=$GCP_PROJECT \
    -e GCS_BUCKET_URI=$GCS_BUCKET_URI \
    -e WANDB_KEY=$WANDB_KEY \ [MAKE SURE YOU HAVE THIS VARIABLE SET]
    $IMAGE_NAME
fi
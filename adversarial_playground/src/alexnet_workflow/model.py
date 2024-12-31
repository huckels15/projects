from kfp import dsl


# Define a Container Component
@dsl.component(
    base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"]
)
def model_training(
    project: str = "",
    location: str = "",
    staging_bucket: str = "",
    bucket_name: str = "",
    epochs: int = 1,
    batch_size: int = 32,
    model_name: str = "alexnet",
    wandb_key:str = '16',
):
    print("Model Training Job")

    import google.cloud.aiplatform as aip

    # Initialize Vertex AI SDK for Python
    aip.init(project=project, location=location, staging_bucket=staging_bucket)

    container_uri = "us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-14.py310:latest"
    python_package_gcs_uri = f"{staging_bucket}/alexnet-trainer.tar.gz"

    job = aip.CustomPythonPackageTrainingJob(
        display_name="alexnet-training",
        python_package_gcs_uri=python_package_gcs_uri,
        python_module_name="alexnet-trainer.train_alexnet",
        container_uri=container_uri,
        project=project,
    )

    CMDARGS = [
        f"--epochs={epochs}",
        f"--batch_size={batch_size}",
        f"--model_name={model_name}",
        f"--model_bucket={bucket_name}",
        f"--wandb_key={wandb_key}"
    ]

    MODEL_DIR = staging_bucket
    TRAIN_COMPUTE = "n1-highmem-8"
    TRAIN_GPU = "NVIDIA_TESLA_T4"
    TRAIN_NGPU = 1

    print(python_package_gcs_uri)

    # Run the training job on Vertex AI
    #sync=True, # If you want to wait for the job to finish
    job.run(
        model_display_name=None,
        args=CMDARGS,
        replica_count=1,
        machine_type=TRAIN_COMPUTE,
        accelerator_type=TRAIN_GPU,
        accelerator_count=TRAIN_NGPU,
        base_output_dir=MODEL_DIR,
        sync=True,
    )

# Define a Container Component
@dsl.component(
    base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"]
)
def adv_model_training(
    project: str = "",
    location: str = "",
    staging_bucket: str = "",
    bucket_name: str = "",
    epochs: int = 1,
    batch_size: int = 32,
    model_name: str = "alexnet_pgd_at",
    wandb_key:str = '16',
):
    print("Adversarial Model Training Job")

    import google.cloud.aiplatform as aip

    # Initialize Vertex AI SDK for Python
    aip.init(project=project, location=location, staging_bucket=staging_bucket)

    container_uri = "us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-14.py310:latest"
    python_package_gcs_uri = f"{staging_bucket}/pgd-at-alexnet-trainer.tar.gz"

    job = aip.CustomPythonPackageTrainingJob(
        display_name="alexnet-training",
        python_package_gcs_uri=python_package_gcs_uri,
        python_module_name="pgd-at-alexnet-trainer.train_pgd_at_alexnet",
        container_uri=container_uri,
        project=project,
    )

    CMDARGS = [
        f"--epochs={epochs}",
        f"--batch_size={batch_size}",
        f"--model_name={model_name}",
        f"--model_bucket={bucket_name}",
        f"--wandb_key={wandb_key}"
    ]

    MODEL_DIR = staging_bucket
    TRAIN_COMPUTE = "n1-highmem-8"
    TRAIN_GPU = "NVIDIA_TESLA_T4"
    TRAIN_NGPU = 1

    print(python_package_gcs_uri)

    # Run the training job on Vertex AI
    # sync=True, # If you want to wait for the job to finish
    job.run(
        model_display_name=None,
        args=CMDARGS,
        replica_count=1,
        machine_type=TRAIN_COMPUTE,
        accelerator_type=TRAIN_GPU,
        accelerator_count=TRAIN_NGPU,
        base_output_dir=MODEL_DIR,
        sync=True,
    )


# Define a Container Component
@dsl.component(
    base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"]
)
def model_deploy(
    bucket_name: str = "",
):
    print("Model Deploy Job")

    import google.cloud.aiplatform as aip

    # List of prebuilt containers for prediction
    # https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
    serving_container_image_uri = (
        "us-docker.pkg.dev/vertex-ai/prediction/tf2-gpu.2-12:latest"
    )

    display_name = "alexnet Model"
    ARTIFACT_URI = f"gs://{bucket_name}/alexnet"

    # Upload and Deploy model to Vertex AI
    # Reference: https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_upload
    deployed_model = aip.Model.upload(
        display_name=display_name,
        artifact_uri=ARTIFACT_URI,
        serving_container_image_uri=serving_container_image_uri,
    )
    print("deployed_model:", deployed_model)
    # Reference: https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_deploy
    endpoint = deployed_model.deploy(
        deployed_model_display_name=display_name,
        traffic_split={"0": 100},
        machine_type="n1-standard-4",
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1,
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )
    print("endpoint:", endpoint)

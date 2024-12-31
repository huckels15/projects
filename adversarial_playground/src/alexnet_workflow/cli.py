import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
from model import model_training as model_training_job, adv_model_training as adv_model_training_job, model_deploy as model_deploy_job


GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME_NORM = os.environ["GCS_BUCKET_NAME_NORM"]
GCS_BUCKET_NAME_ADV= os.environ["GCS_BUCKET_NAME_ADV"]
BUCKET_URI_NORM = f"gs://{GCS_BUCKET_NAME_NORM}"
BUCKET_URI_ADV = f"gs://{GCS_BUCKET_NAME_ADV}"
PIPELINE_ROOT_NORM = f"{BUCKET_URI_NORM}/pipeline_root/root"
PIPELINE_ROOT_ADV = f"{BUCKET_URI_ADV}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
GCS_PACKAGE_URI_NORM = os.environ["GCS_PACKAGE_URI_NORM"]
GCS_PACKAGE_URI_ADV = os.environ["GCS_PACKAGE_URI_ADV"]
GCP_REGION = os.environ["GCP_REGION"]
WANDB_KEY = os.environ["WANDB_KEY"]

DATA_IMAGE = "huckels15/ap-alexnet-data:latest"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def data_download():
    print("data_download()")

    # Define a Container Component
    @dsl.container_component
    def data_download():
        container_spec = dsl.ContainerSpec(
            image=DATA_IMAGE,
            command=[],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def data_download_pipeline():
        data_download()

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        data_download_pipeline, package_path="data_collector.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI_NORM)

    job_id = generate_uuid()
    DISPLAY_NAME = "alexnet-data-download-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="data_collector.yaml",
        pipeline_root=PIPELINE_ROOT_NORM,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)

def model_training():
    print("model_training()")

    @dsl.pipeline
    def model_training_pipeline():
        model_training_job(
            project=GCP_PROJECT,
            location=GCP_REGION,
            staging_bucket=GCS_PACKAGE_URI_NORM,
            bucket_name=GCS_BUCKET_NAME_NORM,
            wandb_key=WANDB_KEY,
        )

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        model_training_pipeline, package_path="model_training.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI_NORM)

    job_id = generate_uuid()
    DISPLAY_NAME = "black-knights-alexnet-training-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="model_training.yaml",
        pipeline_root=PIPELINE_ROOT_NORM,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)

def adv_model_training():
    print("model_training()")

    @dsl.pipeline
    def model_training_pipeline():
        adv_model_training_job(
            project=GCP_PROJECT,
            location=GCP_REGION,
            staging_bucket=GCS_PACKAGE_URI_ADV,
            bucket_name=GCS_BUCKET_NAME_ADV,
            wandb_key=WANDB_KEY,
        )

    # Build yaml file for pipeline
    compiler.Compiler().compile(
        model_training_pipeline, package_path="adv_model_training.yaml"
    )

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI_ADV)

    job_id = generate_uuid()
    DISPLAY_NAME = "black-knights-adv-alexnet-training-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="adv_model_training.yaml",
        pipeline_root=PIPELINE_ROOT_ADV,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def pipeline():
    print("pipeline()")
    # Define a Pipeline
    @dsl.container_component
    def data_download():
        container_spec = dsl.ContainerSpec(
            image=DATA_IMAGE
        )
        return container_spec

    @dsl.pipeline
    def ml_pipeline():
        data_download_task = (
            data_download()
            .set_display_name("Data Download")
        )
        # Normal Model Training
        model_training_task = (
            model_training_job(
                project=GCP_PROJECT,
                location=GCP_REGION,
                staging_bucket=GCS_PACKAGE_URI_NORM,
                bucket_name=GCS_BUCKET_NAME_NORM,
                wandb_key=WANDB_KEY,
            )
            .set_display_name("Model Training")
            .after(data_download_task)
        )
        # Adversarial Fine-Tuning
        adv_model_training_task = (
            adv_model_training_job(
                project=GCP_PROJECT,
                location=GCP_REGION,
                staging_bucket=GCS_PACKAGE_URI_ADV,
                bucket_name=GCS_BUCKET_NAME_ADV,
                wandb_key=WANDB_KEY,
            )
            .set_display_name("Adversarial Fine-Tuning")
            .after(model_training_task)
        )

    # Build yaml file for pipeline
    compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI_NORM)

    job_id = generate_uuid()
    DISPLAY_NAME = "black-knights-combined-pipeline-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="pipeline.yaml",
        pipeline_root=PIPELINE_ROOT_NORM,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def main(args=None):
    print("CLI Arguments:", args)

    if args.pipeline:
        pipeline()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "--pipeline",
        action="store_true",
        help="Black Knights Alexnet Pipeline",
    )
    args = parser.parse_args()

    main(args)

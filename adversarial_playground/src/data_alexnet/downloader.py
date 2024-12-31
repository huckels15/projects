import kagglehub
import os
import kagglehub
from google.cloud import storage

def upload_to_gcp(bucket_name, source_folder, destination_folder=""):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        for root, _, files in os.walk(source_folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, source_folder)
                blob_path = os.path.join(destination_folder, relative_path)

                blob = bucket.blob(blob_path)
                blob.upload_from_filename(local_path)
                print(f"Uploaded {local_path} to gs://{bucket_name}/{blob_path}")

    except Exception as e:
        print(f"An error occurred while uploading to GCP: {e}")

def download_gtsrb_and_upload_to_gcp(bucket_name):
    try:
        path = kagglehub.dataset_download("meowmeowmeowmeowmeow/gtsrb-german-traffic-sign")
        print("Path to dataset files:", path)

        upload_to_gcp(bucket_name, path, destination_folder="data")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "alexnet-data-wf")
    download_gtsrb_and_upload_to_gcp(BUCKET_NAME)

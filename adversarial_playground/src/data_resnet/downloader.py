import kagglehub
import os
from google.cloud import storage

def upload_file_to_gcp(bucket_name, local_file_path, destination_blob_name):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(local_file_path)
        print(f"Uploaded {local_file_path} to gs://{bucket_name}/{destination_blob_name}")
    except Exception as e:
        print(f"An error occurred while uploading to GCP: {e}")

def download_and_upload_hmnist_csv(bucket_name):
    try:
        path = kagglehub.dataset_download("kmader/skin-cancer-mnist-ham10000")
        print("Path to dataset files:", path)

        target_file = os.path.join(path, "hmnist_28_28_RGB.csv")
        if not os.path.exists(target_file):
            print(f"Error: {target_file} not found in the dataset folder.")
            return
        
        destination_blob_name = "data/hmnist_28_28_RGB.csv"
        upload_file_to_gcp(bucket_name, target_file, destination_blob_name)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "resnet-data-wf")
    download_and_upload_hmnist_csv(BUCKET_NAME)


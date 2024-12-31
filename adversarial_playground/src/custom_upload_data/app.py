from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
import os
import shutil
import numpy as np
from typing import Optional, List
import zipfile


GCS_BUCKET_NAME = "custom-attacks-multi"

# FastAPI app setup
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_file_to_gcs(bucket_name: str, local_file_path: str, gcs_blob_path: str):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_filename(local_file_path)

@app.get("/")
def health_check():
    """
    Health check route.
    """
    return {"status": "healthy"}

@app.post("/predict/")
def upload_directory(file: List[UploadFile] = File(...)):
    """
    Upload zip, unzip locally, and upload the unzipped files with directory structure to GCS.
    """
    temp_path = "./temp_model"
    os.makedirs(temp_path, exist_ok=True)

    # Save uploaded zip file locally
    zip_path = os.path.join(temp_path, file[0].filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file[0].file, buffer)

    # Unzip the file locally
    extract_path = os.path.join(temp_path, "unzipped")
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Upload each file and folder in the extracted zip to GCS
    gcs_folder = "run/"
    for root, dirs, files in os.walk(extract_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(local_file_path, extract_path)
            gcs_file_path = os.path.join(gcs_folder, relative_path)
            upload_file_to_gcs(GCS_BUCKET_NAME, local_file_path, gcs_file_path)

    # Clean up local temp files after uploading
    shutil.rmtree(temp_path)

    return {"message": f"Contents uploaded to GCS with directory structure under '{gcs_folder}'"}
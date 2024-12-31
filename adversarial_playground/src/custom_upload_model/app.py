from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
def upload_model(file: UploadFile = File(...)):
    """
    Upload model to local storage and then to GCS.
    """
    model_path = "./uploads/"
    os.makedirs(model_path, exist_ok=True)

    local_model_file = os.path.join(model_path, file.filename)
    with open(local_model_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    gcs_folder = f"run/"
    gcs_filepath = os.path.join(gcs_folder, file.filename)
    upload_file_to_gcs(GCS_BUCKET_NAME, local_model_file, gcs_filepath)
    return {"message": f"Model uploaded to {gcs_folder}"}

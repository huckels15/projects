from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import storage
import os
import shutil
import numpy as np
from typing import Optional, List
import zipfile

# Google Cloud Storage configuration
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'
GCS_BUCKET_NAME = "custom-attacks"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

class AttackRequest(BaseModel):
    model: str
    attack: str
    epsilon: Optional[float] = None
    eps_step: Optional[float] = None
    max_iter: Optional[int] = None

@app.get("/")
def health_check():
    """
    Health check route.
    """
    return {"status": "healthy"}

@app.post("/predict/")
async def predict(payload: dict):
    """
    Perform predictions using the uploaded model and dataset.
    """
    instances = payload.get("instances")
    if not instances or not isinstance(instances, list) or len(instances) == 0:
        raise HTTPException(status_code=400, detail="Invalid payload format. Expected 'instances' as a non-empty list.")

    instance = instances[0]

    try:
        request = AttackRequest(**instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid instance format: {str(e)}")

    # Example: Use GCS paths for the uploaded model and dataset
    model_gcs_path = f"gs://{GCS_BUCKET_NAME}/run/"
    dataset_gcs_path = f"gs://{GCS_BUCKET_NAME}/run//"

    # Replace this logic with your actual prediction script
    result = {
        "model": model_gcs_path,
        "dataset": dataset_gcs_path,
        "attack": request.attack,
        "epsilon": request.epsilon,
        "status": "Prediction completed"
    }

    return {"result": result}

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from io import BytesIO
from unittest.mock import MagicMock
import os
from custom_upload_model.app import app, upload_file_to_gcs

@pytest.fixture
def mock_gcs_upload(monkeypatch):
    mock_upload = MagicMock()
    monkeypatch.setattr("custom_upload_model.app.upload_file_to_gcs", mock_upload)
    return mock_upload

@pytest.fixture
def client():
    client = TestClient(app)
    return client

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_model(client, mock_gcs_upload):
    file_content = b"fake model data"
    mock_file = BytesIO(file_content)
    mock_file.filename = "model.h5"

    response = client.post("/predict/", files={"file": ("model.h5", mock_file, "application/zip")})


    assert response.status_code == 200
    assert response.json() == {"message": "Model uploaded to run/"}

    mock_gcs_upload.assert_called_once_with(
        "custom-attacks-multi", 
        os.path.join("./uploads", "model.h5"),  
        "run/model.h5" 
    )

def test_upload_model_file_not_found(client):
    response = client.post("/predict/")
    assert response.status_code == 422 
    assert "detail" in response.json()

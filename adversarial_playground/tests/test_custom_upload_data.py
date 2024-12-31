import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from unittest.mock import MagicMock
import os
import zipfile
import shutil

from custom_upload_data.app import app, upload_file_to_gcs

@pytest.fixture
def mock_gcs_upload(monkeypatch):
    mock_upload = MagicMock()
    monkeypatch.setattr("custom_upload_data.app.upload_file_to_gcs", mock_upload)
    return mock_upload

@pytest.fixture
def client():
    client = TestClient(app)
    return client

def create_zip_file(file_names):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for name in file_names:
            zip_file.writestr(name, f"Fake content of {name}")
    zip_buffer.seek(0)
    return zip_buffer

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_zip(client, mock_gcs_upload):
    zip_file = create_zip_file(['file1.txt', 'folder1/file2.txt'])

    response = client.post("/predict/", files={"file": ("model.zip", zip_file, "application/zip")})

    assert response.status_code == 200
    assert response.json() == {"message": "Contents uploaded to GCS with directory structure under 'run/'"}

    mock_gcs_upload.assert_any_call(
        "custom-attacks-multi", 
        os.path.join("./temp_model", "unzipped", "file1.txt"), 
        "run/file1.txt" 
    )
    mock_gcs_upload.assert_any_call(
        "custom-attacks-multi", 
        os.path.join("./temp_model", "unzipped", "folder1", "file2.txt"), 
        "run/folder1/file2.txt"
    )


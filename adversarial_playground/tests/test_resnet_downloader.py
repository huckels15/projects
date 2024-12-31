import pytest
from unittest import mock
import os
from data_resnet.downloader import upload_file_to_gcp, download_and_upload_hmnist_csv

@mock.patch("google.cloud.storage.Client")
@mock.patch("google.cloud.storage.Blob.upload_from_filename")
def test_upload_file_to_gcp(mock_upload, mock_storage_client):
    mock_bucket = mock.Mock()
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_blob = mock.Mock()
    mock_bucket.blob.return_value = mock_blob

    local_file_path = '/mock/path/to/file.csv'
    destination_blob_name = 'data/file.csv'

    upload_file_to_gcp('mock-bucket', local_file_path, destination_blob_name)

    mock_storage_client.assert_called_once()
    mock_bucket.blob.assert_called_once_with(destination_blob_name)
    mock_blob.upload_from_filename.assert_called_once_with(local_file_path)
    print("Upload file to GCP test passed.")


@mock.patch("kagglehub.dataset_download")
@mock.patch("os.path.exists")
@mock.patch("data_resnet.downloader.upload_file_to_gcp")
def test_download_and_upload_hmnist_csv(mock_upload, mock_exists, mock_dataset_download):
    mock_dataset_download.return_value = "/mock/path/to/dataset"
    
    mock_exists.return_value = True

    download_and_upload_hmnist_csv("mock-bucket")

    mock_dataset_download.assert_called_once_with("kmader/skin-cancer-mnist-ham10000")
    mock_exists.assert_called_once_with("/mock/path/to/dataset/hmnist_28_28_RGB.csv")
    mock_upload.assert_called_once_with("mock-bucket", "/mock/path/to/dataset/hmnist_28_28_RGB.csv", "data/hmnist_28_28_RGB.csv")
    print("Download and upload HMNIST CSV test passed.")


import pytest
from unittest import mock
from google.cloud import storage
import os

from data_alexnet.downloader import upload_to_gcp, download_gtsrb_and_upload_to_gcp


@mock.patch("google.cloud.storage.Client")
@mock.patch("os.walk")
def test_upload_to_gcp(mock_os_walk, mock_storage_client):
    mock_os_walk.return_value = [
        ('/source/folder', [], ['file1.txt', 'file2.txt'])
    ]
    
    mock_bucket = mock.Mock()
    mock_storage_client.return_value.bucket.return_value = mock_bucket

    mock_blob = mock.Mock()
    mock_bucket.blob.return_value = mock_blob   

    upload_to_gcp('mock-bucket', '/source/folder')

    mock_storage_client.assert_called_once()
    mock_bucket.blob.assert_any_call("file1.txt")
    mock_bucket.blob.assert_any_call("file2.txt")
    mock_blob.upload_from_filename.assert_any_call('/source/folder/file1.txt')
    mock_blob.upload_from_filename.assert_any_call('/source/folder/file2.txt')
    print("Upload test passed.")




@mock.patch("kagglehub.dataset_download")
@mock.patch("data_alexnet.downloader.upload_to_gcp")
def test_download_gtsrb_and_upload_to_gcp(mock_upload, mock_dataset_download):
    mock_dataset_download.return_value = "/mock/path/to/gtsrb"
    
    download_gtsrb_and_upload_to_gcp("mock-bucket")

    mock_dataset_download.assert_called_once_with("meowmeowmeowmeowmeow/gtsrb-german-traffic-sign")
    mock_upload.assert_called_once_with("mock-bucket", "/mock/path/to/gtsrb", destination_folder="data")
    print("Download and upload test passed.")

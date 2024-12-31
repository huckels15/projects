import pytest
from unittest.mock import MagicMock, patch
import numpy as np
import tensorflow as tf
from art_attacks.custom_attacks.custom_attacks import *
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent as PGD, DeepFool, SquareAttack as Square
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import pandas as pd

IMG_HEIGHT, IMG_WIDTH = 224, 224
NUM_CLASSES = 7

MG_HEIGHT, IMG_WIDTH = 224, 224
NUM_CLASSES = 7

@pytest.fixture
def mock_os_listdir(monkeypatch):
    def mock_listdir(path):
        if path == 'mock_data_path':
            return ['class1', 'class2']  
        if path == 'mock_model_path':
            return ['model.h5']  
    monkeypatch.setattr(os, 'listdir', mock_listdir)


@pytest.fixture
def mock_cv2(monkeypatch):

    def mock_imread(path, flags):
        return np.random.rand(224, 224, 3)  

    monkeypatch.setattr(cv2, 'imread', mock_imread)

@pytest.fixture
def mock_concatenate(monkeypatch):
    def mock_concatenate(arrays, axis=0):
        return np.random.rand(2, 224, 224, 3)

    monkeypatch.setattr(np, 'concatenate', mock_concatenate)


@pytest.fixture
def mock_preprocess_data(mock_os_listdir, mock_cv2):
    data_path = 'mock_data_path'
    batch_size = 32
    img_height = 224
    img_width = 224
    channels = 3
    
    x_batch_1 = np.random.rand(batch_size, img_height, img_width, channels)
    y_batch_1 = np.random.randint(0, 7, size=(batch_size,))
    
    x_batch_2 = np.random.rand(batch_size, img_height, img_width, channels)
    y_batch_2 = np.random.randint(0, 7, size=(batch_size,))

    def mock_data_generator():
        yield x_batch_1, y_batch_1  
        yield x_batch_2, y_batch_2  

    return mock_data_generator

@pytest.fixture
def mock_read_csv(monkeypatch):

    def mock_csv(*args, **kwargs):
        return pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    monkeypatch.setattr(pd, 'read_csv', mock_csv)

@pytest.fixture
def mock_model(monkeypatch):
    model = Sequential([
        Flatten(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        Dense(128, activation='relu'),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    monkeypatch.setattr("tensorflow.keras.models.load_model", lambda *args, **kwargs: model)
    return model

@patch("shutil.rmtree")
@patch("os.path.exists")
def test_cleanup_temp_dirs(mock_exists, mock_rmtree):

    mock_exists.side_effect = lambda dir: dir in ["dir1", "dir2"]  

    cleanup_temp_dirs("dir1", "dir2", "dir3")

    mock_rmtree.assert_any_call("dir1")
    mock_rmtree.assert_any_call("dir2")

@patch("google.cloud.storage.Client")
@patch("os.makedirs")
@patch("os.path.exists")
@patch("google.cloud.storage.Blob.download_to_filename")
def test_download_from_gcs(mock_download_to_filename, mock_exists, mock_makedirs, mock_storage_client):
    mock_exists.return_value = False  
    
    mock_client = MagicMock()
    mock_storage_client.return_value = mock_client
    mock_bucket = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_blob = MagicMock()
    mock_bucket.list_blobs.return_value = [mock_blob]  

    mock_blob.name = "gs://bucket/prefix/file.txt"

    download_from_gcs("gs://bucket/prefix/file.txt", "/local/path")

    mock_makedirs.assert_called_with("/local/path/../../gs:/bucket/prefix", exist_ok=True)


@patch("google.cloud.storage.Client")
@patch("google.cloud.storage.Blob.download_to_filename")
def test_download_from_gcs_no_blobs(mock_download_to_filename, mock_storage_client):
    mock_client = MagicMock()
    mock_storage_client.return_value = mock_client
    mock_bucket = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = []
    
    with pytest.raises(FileNotFoundError):
        download_from_gcs("gs://bucket/prefix/file.txt", "/local/path")

def test_preprocess_data(mock_preprocess_data):
    data_generator = mock_preprocess_data 
    x_batch, y_batch = next(data_generator())
    
    assert x_batch.shape == (32, 224, 224, 3)  
    assert y_batch.shape == (32,) 


def mock_attack_generate(self, x):
    return np.random.rand(*x.shape)

@pytest.fixture
def mock_plot(monkeypatch):
    def mock_plot_samples(*args, **kwargs):
        return "mocked_path_to_figure.png"
    
    monkeypatch.setattr("art_attacks.custom_attacks.custom_attacks.plot_samples", mock_plot_samples)

@pytest.fixture
def mock_model(monkeypatch):
    model = Sequential([
        Flatten(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        Dense(128, activation='relu'),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    monkeypatch.setattr("tensorflow.keras.models.load_model", lambda *args, **kwargs: model)
    return model

@pytest.fixture
def mock_classifier(monkeypatch):
    mock_classifier = MagicMock()
    mock_classifier.predict.return_value = np.eye(NUM_CLASSES)[:2]
    mock_classifier.generate.return_value = np.random.rand(2, IMG_HEIGHT, IMG_WIDTH, 3)
    monkeypatch.setattr("art.estimators.classification.KerasClassifier", lambda *args, **kwargs: mock_classifier)
    return mock_classifier


def test_parse_args(monkeypatch):

    fake_args = [
        "--fgsm",
        "--eps", "0.3",
        "--max_iter", "10",
        "--model_path", "model_path",
        "--data_path", "data_path",
    ]

    monkeypatch.setattr("sys.argv", ["custom_attacks.py"] + fake_args)
    run_args = parse_args()

    assert run_args["fgsm"] is True
    assert run_args["eps"] == 0.3
    assert run_args["max_iter"] == 10
    assert run_args["data_path"] == "data_path"
    assert run_args["model_path"] == "model_path"


def test_plot_samples(monkeypatch):

    def mock_savefig(path):
        pass

    monkeypatch.setattr("matplotlib.pyplot.savefig", mock_savefig)

    x_test = np.random.rand(1, IMG_HEIGHT, IMG_WIDTH, 3)
    x_test_adv = np.random.rand(1, IMG_HEIGHT, IMG_WIDTH, 3)
    y_test = to_categorical([0], NUM_CLASSES)
    predictions_adv = to_categorical([1], NUM_CLASSES)

    path = plot_samples(1, x_test, x_test_adv, y_test, predictions_adv)

    assert path == "figures/example_1_original_vs_adversarial.png"



def test_run(mock_preprocess_data, mock_os_listdir, mock_concatenate, mock_model, mock_plot, monkeypatch):
    mock_args = MagicMock()
    mock_args.fgsm = False
    mock_args.pgd = True
    mock_args.deepfool = False
    mock_args.square = False
    mock_args.eps = "0.2"
    mock_args.eps_step = "0.01"
    mock_args.max_iter = "50"
    
    mock_run_args = {
        "fgsm": False,
        "pgd": True,
        "deepfool": False,
        "square": False,
        "eps": 0.2,
        "eps_step": 0.01,
        "max_iter": 50,
    }

    results = run("mock_model_path", "mock_data_path", mock_run_args, 28, 28, 1)

    assert results is not None
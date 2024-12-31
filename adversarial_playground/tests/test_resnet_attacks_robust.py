import pytest
from unittest.mock import MagicMock
import numpy as np
import tensorflow as tf
from art_attacks.resnet_attacks.resnet_attacks import *
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent as PGD, DeepFool, SquareAttack as Square
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

IMG_HEIGHT, IMG_WIDTH = 224, 224
NUM_CLASSES = 7


@pytest.fixture
def mock_load_data():
    X = np.random.rand(110, 224, 224, 3) 
    y = np.random.randint(0, 7, size=(110,)) 
    y = tf.keras.utils.to_categorical(y, num_classes=7)
    
    return MagicMock(), MagicMock(), (X, y)

@pytest.fixture
def mock_load_model(path, custom_objects=None, compile=True):
    model = MagicMock()
    model.compile = MagicMock()
    model.predict = MagicMock(return_value=np.random.randint(0, 7, size=(10, 7)))  # Mock predictions
    return model

def mock_attack_generate(self, x):
    return np.random.rand(*x.shape)

@pytest.fixture
def mock_read_csv(monkeypatch):
    def mock_csv(*args, **kwargs):
        mock_labels = np.random.randint(0, 7, size=(110,)) 
        mock_data = np.random.rand(110, 28, 28, 3).reshape(110, -1)
        mock_df = MagicMock()
        mock_df = pd.DataFrame(mock_data, columns=[f'pixel_{i}' for i in range(mock_data.shape[1])])
        mock_df['label'] = mock_labels 
        return mock_df
    monkeypatch.setattr('pandas.read_csv', mock_csv)


@pytest.fixture
def mock_plot(monkeypatch):
    def mock_plot_samples(*args, **kwargs):
        return "mocked_path_to_figure.png"
    
    monkeypatch.setattr("art_attacks.resnet_attacks.resnet_attacks.plot_samples", mock_plot_samples)

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


def test_load_data(mock_read_csv, monkeypatch):
    
    test_gen = load_data()
    
    assert test_gen is not None

def test_parse_args(monkeypatch):

    fake_args = [
        "--fgsm",
        "--eps", "0.3",
        "--max_iter", "10"
    ]

    monkeypatch.setattr("sys.argv", ["resnet_attacks.py"] + fake_args)
    args, run_args = parse_args()

    assert args.fgsm is True
    assert run_args["eps"] == "0.3"
    assert run_args["max_iter"] == "10"


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


def test_run(mock_read_csv, mock_model, mock_plot, mock_classifier, monkeypatch):

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
        "eps": "0.2",
        "eps_step": "0.01",
        "max_iter": "50"
    }

    monkeypatch.setattr("art_attacks.resnet_attacks.resnet_attacks.parse_args", lambda: (mock_args, mock_run_args))
    results = run(mock_args, mock_run_args)

    assert "reg_acc" in results
    assert "adv_acc" in results
    assert "figure" in results

    assert isinstance(results["reg_acc"], float)
    assert isinstance(results["adv_acc"], float)
    assert results["figure"] == "mocked_path_to_figure.png"

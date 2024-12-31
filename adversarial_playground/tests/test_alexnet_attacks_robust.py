import pytest
import numpy as np
from unittest.mock import MagicMock
from art_attacks.robust_alexnet_attacks.robust_alexnet_attacks import *
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

IMG_HEIGHT, IMG_WIDTH = 32, 32
NUM_CLASSES = 43


@pytest.fixture
def mock_generator(monkeypatch):
    def mock_gen(*args, **kwargs):
        x_mock = np.random.rand(2, IMG_HEIGHT, IMG_WIDTH, 3)
        y_mock = np.eye(NUM_CLASSES)[:2] 
        yield x_mock, y_mock

    monkeypatch.setattr("art_attacks.robust_alexnet_attacks.robust_alexnet_attacks.generator", mock_gen)

@pytest.fixture
def mock_plot(monkeypatch):
    def mock_plot_samples(*args, **kwargs):
        return "mocked_path_to_figure.png"
    
    monkeypatch.setattr("art_attacks.robust_alexnet_attacks.robust_alexnet_attacks.plot_samples", mock_plot_samples)

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


def test_generator(monkeypatch, tmpdir):
    base_path = tmpdir.mkdir("data")
    for class_id in range(NUM_CLASSES):
        class_dir = base_path.mkdir(str(class_id))
        for i in range(5):
            img_path = class_dir.join(f"img_{i}.jpg")
            np.random.rand(IMG_HEIGHT, IMG_WIDTH, 3).astype(np.uint8).tofile(str(img_path))

    def mock_imread(path):
        return np.random.rand(IMG_HEIGHT, IMG_WIDTH, 3) * 255

    def mock_resize(img, size):
        return np.random.rand(size[0], size[1], 3)

    monkeypatch.setattr("cv2.imread", mock_imread)
    monkeypatch.setattr("cv2.resize", mock_resize)

    gen = generator(str(base_path), batch_size=2)

    for x_batch, y_batch in gen:
        assert x_batch.shape[0] <= 2
        assert x_batch.shape[1:] == (IMG_HEIGHT, IMG_WIDTH, 3)
        assert y_batch.shape[1] == NUM_CLASSES
        break
    
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

def test_parse_args(monkeypatch):

    fake_args = [
        "--fgsm",
        "--eps", "0.3",
        "--max_iter", "10"
    ]

    monkeypatch.setattr("sys.argv", ["alexnet_attacks.py"] + fake_args)
    args, run_args = parse_args()

    assert args.fgsm is True
    assert run_args["eps"] == "0.3"
    assert run_args["max_iter"] == "10"

def test_run(mock_model, mock_generator, mock_plot, mock_classifier, monkeypatch):

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

    monkeypatch.setattr("art_attacks.robust_alexnet_attacks.robust_alexnet_attacks.parse_args", lambda: (mock_args, mock_run_args))
    results = run(mock_args, mock_run_args)

    assert "reg_acc" in results
    assert "adv_acc" in results
    assert "figure" in results

    assert isinstance(results["reg_acc"], float)
    assert isinstance(results["adv_acc"], float)
    assert results["figure"] == "mocked_path_to_figure.png"

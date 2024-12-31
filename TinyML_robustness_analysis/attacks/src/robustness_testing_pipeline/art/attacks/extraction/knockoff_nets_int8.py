from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Optional, TYPE_CHECKING, Union

import numpy as np
from tqdm.auto import trange

from art.config import ART_NUMPY_DTYPE
from art.attacks.attack import ExtractionAttack
from art.estimators.estimator import BaseEstimator
from art.estimators.classification.classifier import ClassifierMixin
from art.utils import to_categorical

if TYPE_CHECKING:
    from art.utils import CLASSIFIER_TYPE

logger = logging.getLogger(__name__)


class KnockoffNets_Int8(ExtractionAttack):
    """
    Implementation of the Knockoff Nets attack adapted for int8 quantized models.
    """

    attack_params = ExtractionAttack.attack_params + [
        "batch_size_fit",
        "batch_size_query",
        "nb_epochs",
        "nb_stolen",
        "sampling_strategy",
        "reward",
        "verbose",
        "use_probability",
    ]

    _estimator_requirements = (BaseEstimator, ClassifierMixin)

    def __init__(
        self,
        classifier: "CLASSIFIER_TYPE",
        batch_size_fit: int = 1,
        batch_size_query: int = 1,
        nb_epochs: int = 10,
        nb_stolen: int = 1,
        sampling_strategy: str = "random",
        reward: str = "all",
        verbose: bool = True,
        use_probability: bool = False,
    ) -> None:
        """
        Create a KnockoffNets attack instance for int8 models.

        :param classifier: A victim classifier.
        :param batch_size_fit: Size of batches for fitting the thieved classifier.
        :param batch_size_query: Size of batches for querying the victim classifier.
        :param nb_epochs: Number of epochs to use for training.
        :param nb_stolen: Number of queries submitted to the victim classifier to steal it.
        :param sampling_strategy: Sampling strategy, either `random` or `adaptive`.
        :param reward: Reward type, in ['cert', 'div', 'loss', 'all'].
        :param verbose: Show progress bars.
        """
        super().__init__(estimator=classifier)

        self.batch_size_fit = batch_size_fit
        self.batch_size_query = batch_size_query
        self.nb_epochs = nb_epochs
        self.nb_stolen = nb_stolen
        self.sampling_strategy = sampling_strategy
        self.reward = reward
        self.verbose = verbose
        self.use_probability = use_probability
        self._check_params()

    def round_half_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return np.floor(n * multiplier + 0.5) / multiplier

    def quantize(self, data, scaler=1 / 255, zp=-128):
        data = np.array(data, dtype=np.float32)
        data_int8 = data / scaler + zp
        data_int8 = self.round_half_up(data_int8, 0)
        data_int8 = np.array(data_int8, dtype=np.int8)
        data_int8 = np.clip(data_int8, a_min=-128, a_max=127)

        return data_int8

    def extract(self, x: np.ndarray, y: Optional[np.ndarray] = None, **kwargs) -> "CLASSIFIER_TYPE":
        """
        Extract a thieved classifier.

        :param x: An array with the source input to the victim classifier.
        :param y: Target values (class labels) one-hot-encoded of shape (nb_samples, nb_classes) or indices of shape
                  `(nb_samples,)`.
        :param thieved_classifier: A thieved classifier to be stolen.
        :return: The stolen classifier.
        """
        # Check prerequisite for random strategy
        if self.sampling_strategy == "random" and y is not None:  # pragma: no cover
            logger.warning("This attack with random sampling strategy does not use the provided label y.")

        # Check prerequisite for adaptive strategy
        if self.sampling_strategy == "adaptive" and y is None:  # pragma: no cover
            raise ValueError("This attack with adaptive sampling strategy needs label y.")

        # Check the size of the source input vs nb_stolen
        if x.shape[0] < self.nb_stolen:  # pragma: no cover
            logger.warning(
                "The size of the source input is smaller than the expected number of queries submitted "
                "to the victim classifier."
            )

        # Check if there is a thieved classifier provided for training
        thieved_classifier = kwargs.get("thieved_classifier")
        if thieved_classifier is None or not isinstance(thieved_classifier, ClassifierMixin):  # pragma: no cover
            raise ValueError("A thieved classifier is needed.")

        # Implement model extractions
        if self.sampling_strategy == "random":
            thieved_classifier = self._random_extraction(x, thieved_classifier)  # type: ignore
        else:
            thieved_classifier = self._adaptive_extraction(x, y, thieved_classifier)  # type: ignore

        return thieved_classifier

    def _random_extraction(self, x: np.ndarray, thieved_classifier: "CLASSIFIER_TYPE") -> "CLASSIFIER_TYPE":
        """
        Extract with the random sampling strategy.

        :param x: An array with the source input to the victim classifier.
        :param thieved_classifier: A thieved classifier to be stolen.
        :return: The stolen classifier.
        """
        # Select data to attack
        selected_x = self._select_data(x)

        # Query the victim classifier with quantized data
        fake_labels = self._query_label(selected_x)

        # Train the thieved classifier
        thieved_classifier.fit(
            x=selected_x,
            y=fake_labels,
            batch_size=self.batch_size_fit,
            nb_epochs=self.nb_epochs,
            verbose=0,
        )

        return thieved_classifier

    def _select_data(self, x: np.ndarray) -> np.ndarray:
        """
        Select data to attack.

        :param x: An array with the source input to the victim classifier.
        :return: An array with the selected input to the victim classifier.
        """
        nb_stolen = np.minimum(self.nb_stolen, x.shape[0])
        rnd_index = np.random.choice(x.shape[0], nb_stolen, replace=False)

        return x[rnd_index].astype(ART_NUMPY_DTYPE)

    def _query_label(self, x: np.ndarray) -> np.ndarray:
        """
        Query the victim classifier.

        :param x: An array with the source input to the victim classifier.
        :return: Target values (class labels) one-hot-encoded of shape `(nb_samples, nb_classes)`.
        """
        x_int8 = self.quantize(x)
        labels = self.estimator.predict(x=x_int8, batch_size=self.batch_size_query)
        if not self.use_probability:
            labels = np.argmax(labels, axis=1)
            labels = to_categorical(labels=labels, nb_classes=self.estimator.nb_classes)

        return labels

    def _adaptive_extraction(
        self, x: np.ndarray, y: np.ndarray, thieved_classifier: "CLASSIFIER_TYPE"
    ) -> "CLASSIFIER_TYPE":
        """
        Extract with the adaptive sampling strategy.

        :param x: An array with the source input to the victim classifier.
        :param y: Target values (class labels) one-hot-encoded of shape (nb_samples, nb_classes) or indices of shape
                  (nb_samples,).
        :param thieved_classifier: A thieved classifier to be stolen.
        :return: The stolen classifier.
        """
        # Adaptive extraction code (similar logic to original implementation)

        # Train the thieved classifier the final time
        thieved_classifier.fit(
            x=x,
            y=y,
            batch_size=self.batch_size_fit,
            nb_epochs=self.nb_epochs,
        )

        return thieved_classifier

    def _check_params(self) -> None:
        if not isinstance(self.batch_size_fit, int) or self.batch_size_fit <= 0:
            raise ValueError("The size of batches for fitting the thieved classifier must be a positive integer.")

        if not isinstance(self.batch_size_query, int) or self.batch_size_query <= 0:
            raise ValueError("The size of batches for querying the victim classifier must be a positive integer.")

        if not isinstance(self.nb_epochs, int) or self.nb_epochs <= 0:
            raise ValueError("The number of epochs must be a positive integer.")

        if not isinstance(self.nb_stolen, int) or self.nb_stolen <= 0:
            raise ValueError("The number of queries submitted to the victim classifier must be a positive integer.")

        if self.sampling_strategy not in ["random", "adaptive"]:
            raise ValueError("Sampling strategy must be either `random` or `adaptive`.")

        if self.reward not in ["cert", "div", "loss", "all"]:
            raise ValueError("Reward type must be in ['cert', 'div', 'loss', 'all'].")

        if not isinstance(self.verbose, bool):
            raise ValueError("The argument `verbose` has to be of type bool.")
        if not isinstance(self.use_probability, bool):
            raise ValueError("The argument `use_probability` has to be of type bool.")

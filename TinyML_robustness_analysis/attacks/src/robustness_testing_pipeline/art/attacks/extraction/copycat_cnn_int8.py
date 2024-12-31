from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import Optional, TYPE_CHECKING

import numpy as np

from art.config import ART_NUMPY_DTYPE
from art.attacks.attack import ExtractionAttack
from art.estimators.estimator import BaseEstimator
from art.estimators.classification.classifier import ClassifierMixin
from art.utils import to_categorical

if TYPE_CHECKING:
    from art.utils import CLASSIFIER_TYPE

logger = logging.getLogger(__name__)

class CopycatCNN_Int8(ExtractionAttack):
    """
    Implementation of the Copycat CNN attack from Rodrigues Correia-Silva et al. (2018) for int8 models.

    | Paper link: https://arxiv.org/abs/1806.05476
    """

    attack_params = ExtractionAttack.attack_params + [
        "batch_size_fit",
        "batch_size_query",
        "nb_epochs",
        "nb_stolen",
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
        use_probability: bool = False,
    ) -> None:
        """
        Create a Copycat CNN attack instance for int8 models.

        :param classifier: A victim classifier.
        :param batch_size_fit: Size of batches for fitting the thieved classifier.
        :param batch_size_query: Size of batches for querying the victim classifier.
        :param nb_epochs: Number of epochs to use for training.
        :param nb_stolen: Number of queries submitted to the victim classifier to steal it.
        """
        super().__init__(estimator=classifier)

        self.batch_size_fit = batch_size_fit
        self.batch_size_query = batch_size_query
        self.nb_epochs = nb_epochs
        self.nb_stolen = nb_stolen
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
                  (nb_samples,). Not used in this attack.
        :param thieved_classifier: A classifier to be stolen, currently always trained on one-hot labels.
        :type thieved_classifier: :class:`.Classifier`
        :return: The stolen classifier.
        """
        # Warning to users if y is not None
        if y is not None:  # pragma: no cover
            logger.warning("This attack does not use the provided label y.")

        # Check the size of the source input vs nb_stolen
        if x.shape[0] < self.nb_stolen:  # pragma: no cover
            logger.warning(
                "The size of the source input is smaller than the expected number of queries submitted "
                "to the victim classifier."
            )

        # Check if there is a thieved classifier provided for training
        thieved_classifier = kwargs["thieved_classifier"]
        if thieved_classifier is None or not isinstance(thieved_classifier, ClassifierMixin):  # pragma: no cover
            raise ValueError("A thieved classifier is needed.")

        # Select data to attack
        selected_x = self._select_data(x)

        # Query the victim classifier with int8 data
        fake_labels = self._query_label(selected_x)

        # Train the thieved classifier
        thieved_classifier.fit(  # type: ignore
            x=selected_x,
            y=fake_labels,
            batch_size=self.batch_size_fit,
            nb_epochs=self.nb_epochs,
        )

        return thieved_classifier  # type: ignore

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
        :return: Target values (class labels) one-hot-encoded of shape (nb_samples, nb_classes).
        """
        # Quantize the input before querying the classifier
        x_int8 = self.quantize(x)
        labels = self.estimator.predict(x=x_int8, batch_size=self.batch_size_query)
        if not self.use_probability:
            labels = np.argmax(labels, axis=1)
            labels = to_categorical(labels=labels, nb_classes=self.estimator.nb_classes)

        return labels

    def _check_params(self) -> None:
        if not isinstance(self.batch_size_fit, int) or self.batch_size_fit <= 0:
            raise ValueError("The size of batches for fitting the thieved classifier must be a positive integer.")

        if not isinstance(self.batch_size_query, int) or self.batch_size_query <= 0:
            raise ValueError("The size of batches for querying the victim classifier must be a positive integer.")

        if not isinstance(self.nb_epochs, int) or self.nb_epochs <= 0:
            raise ValueError("The number of epochs must be a positive integer.")

        if not isinstance(self.nb_stolen, int) or self.nb_stolen <= 0:
            raise ValueError("The number of queries submitted to the victim classifier must be a positive integer.")

        if not isinstance(self.use_probability, bool):
            raise ValueError("The argument `use_probability` has to be of type bool.")

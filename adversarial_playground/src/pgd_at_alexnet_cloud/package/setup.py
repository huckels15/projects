from setuptools import find_packages
from setuptools import setup


REQUIRED_PACKAGES = ["wandb==0.15.11"]

setup(
    name="alexnet-trainer",
    version="0.0.1",
    install_requires=[
        "tensorflow==2.11.0",
        "numpy",
        "pandas",
        "wandb",
        "adversarial-robustness-toolbox",
        "scikit-learn",
        "google-cloud-storage",
    ],
    packages=find_packages(),
    description="PGD AT Alexnet Trainer",
)
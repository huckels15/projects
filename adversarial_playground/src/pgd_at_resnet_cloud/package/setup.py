from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    "wandb==0.15.11",
    "adversarial-robustness-toolbox",
    "opencv-python"
]

setup(
    name="pgd-at-resnet-trainer",
    version="0.0.1",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="PGD AT ResNet101 Trainer",
)
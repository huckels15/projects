# Resnet Attacks API
## Description
The files in this folder are used to create the Resnet attack API service for our project. It creates a docker container that takes attack specifications from the front end, runs `resnet_attacks.py`, and returns the results of the attack.

## Setup and Usage Instructions

To set up the Resnet attack server, begin by downloading the data at the drive link in our top level `README.md`. This data is just a CSV and must be put in a new directory `/data` within the `resnet_attacks` directory. You can then build the Docker container by running the `docker-shell.sh` script. To build, you must change build variable in the shell script to true. This will put you in the container with a shell. Once in the shell, run `uvicorn app:app --port 8000 --host 0.0.0.0` to start the service locally. To test the server, open a new terminal outside the container and use some of the test termnial commands below:

```
curl -X POST http://127.0.0.1:8000/resnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "resnet", "attack": "fgsm", "epsilon": 0.2}'

curl -X POST http://127.0.0.1:8000/resnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "resnet", "attack": "pgd", "epsilon": 0.2, "eps_step": 0.01, "max_iter": 10}'

curl -X POST http://127.0.0.1:8000/resnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "resnet", "attack": "deepfool", "max_iter": 10}'

curl -X POST http://127.0.0.1:8000/resnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "resnet", "attack": "square", "epsilon": 0.2, "max_iter": 10}'
```

This will make the server execute the given attack for the given model. The `model` parameter specifies the model, the `attack` parameter specifies the attack, and the following arguments seen above specify attack parameters. Running these will return a json output of the following form:

```
{adv_acc: x, reg_acc: x, figure: path/to/before/and/after}
```

Using the `figure` path returned, you can then use the following command to get the plot of the sample
before and after the attack:

```
curl -o example.png "http://127.0.0.1:8000/get-file/?file_path=path/to/before/and/after.png"
```
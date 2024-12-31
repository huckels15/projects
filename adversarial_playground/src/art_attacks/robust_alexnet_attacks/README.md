# Alexnet Attacks API
## Description
The files in this folder are used to create the Alexnet attack API service for our project. It creates a docker container that takes attack specifications from the front end, runs `alexnet_attacks.py`, and returns the results of the attack.

## Setup and Usage Instructions

To set up the Alexnet attack server, begin by building the Docker container by running the 
`docker-shell.sh` script. To build, you must change build variable in the shell script to true. THIS ATTACK ONLY WORKS IN OUR CLOUD VMS AS IT RELIES ON CLOUD DATA. This will put you in the container with a shell. Once in the shell, run the `docker-entrypoint.sh` file to mount the cloud bucket to the data directory. You can then run `uvicorn app:app --port 8000 --host 0.0.0.0` to start the services. To test the server, open a new terminal outside the container and use some of the test termnial commands below:

```
curl -X POST http://127.0.0.1:8000/alexnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "alexnet", "attack": "fgsm", "epsilon": 0.2}'

curl -X POST http://127.0.0.1:8000/alexnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "alexnet", "attack": "pgd", "epsilon": 0.2, "eps_step": 0.01, "max_iter": 10}'

curl -X POST http://127.0.0.1:8000/alexnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "alexnet", "attack": "deepfool", "max_iter": 10}'

curl -X POST http://127.0.0.1:8000/alexnet-attack/ \
-H "Content-Type: application/json" \
-d '{"model": "alexnet", "attack": "square", "epsilon": 0.2, "max_iter": 10}'
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
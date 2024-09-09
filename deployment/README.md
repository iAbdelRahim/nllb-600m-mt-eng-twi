# Deployment

This folder contains the resources required for using the model via api

## Usage

> All commands below are run from this directory.

### Building your model image


1. First, make sure you have the trained model and tokenizer locally available. 

1. Copy over the trained model and its definition code into this folder so that it can be baked into the Docker container for serving

    ```bash
    cp -r ../saved_model .
    ```

1. Then build the container locally and give it a tag

    ```bash
    docker build -t nllb-600m-mt-eng-twi:latest .
    ```

### Local testing

1. either use docker :

    ```bash
    docker compose up -d
    docker compose logs
    ```
    go to the designed link and use the api in your browser

    ```bash
    http://localhost:80/docs
    ```
2. or run the uvicorn server localy (after installing all the dependencies )
    > python -m venv env

    > env/Scripts/Activate  or source env/Scripts/activate

    > pip install -r serve-requirements.txt

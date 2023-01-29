# Search Services

This repository contains the docker-compose file to run the search services. Which are part of the [FIRST Search Engine]() (checkout the main repo [here]()). While the services can be run individually, it is recommended to use the docker-compose file to run the services. The docker-compose file is configured to run the services on a GPU. If you want to run the services on a CPU, you should change the `docker-compose.yml` file.

## Requirements

Make sure that docker-compose version is 1.29.0 or higher. To check the version, run `docker-compose -v`.
To be able to run the services. Docker and docker-compose should be installed on the machine. Nvidia-docker is also required if you want to run the services on a GPU (which is default). To install docker, follow the instructions [here](https://docs.docker.com/engine/install/). To install docker-compose, follow the instructions [here](https://docs.docker.com/compose/install/) and to install nvidia-docker, follow the instructions [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker).

## Configuration

The configuration is done in the `.env` file. Users should change the values of the `*_PORT` variables.

## Start the services

To start the services, run the following command:
```bash
docker-compose up -d
```
## Stop the services
```bash
docker-compose down
```

## Check the status of the services
```bash
docker-compose ps
```

## Check the logs of the services
```bash
docker-compose logs -f
```

## Check the logs of a specific service
```bash
docker-compose logs -f <service-name>
```

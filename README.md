# Search Services

This repository contains the docker-compose file to run the search services. Which are part of the [FIRST Search Engine]() (checkout the main repo [here]()). While the services can be run individually, it is recommended to use the docker-compose file to run the services. The docker-compose file is configured to run the services on a GPU. If you want to run the services on a CPU, you should change the `docker-compose.yml` file.


This repository contains two main parts, first the services which are a set of docker images that are ready to be used. These images configurations are stored in the dotenv file. Checkout the #Configuration section to see how to configure the services. The second part is a `pysearch` package which contains necessary protocols used by the services. The package is also used by the client to communicate with the services.

## PySearch

PySearch is a python wrapper around the search services, used to communicate with the services. 
Currently, the package is not published on PyPI. So, to use the package, you should install it locally. To install the package locally, run the following command:
```bash
$ mamba env create -f services.yml
$ conda activate services
```

At the moment, there are only two search services available, `elastic search` and `milvus` which are used to search for images and text respectively. The package provides a `Processor` class which is used to communicate with the services. To see how to use the package, checkout the `examples` directory [here](examples/).

On the other hand, the package also provides necessary time processing methods. These methods are used to convert the time from the human readable format to `datetime` object; generates useful time formats such as `Monday`, `Weekend`, etc; determines the part of the day such as `morning`, `afternoon`, `evening`, etc; Checkout the `pysearch.ultis.time` file to see the available methods.

## Services

### Requirements

Make sure that docker-compose version is 1.29.0 or higher. To check the version, run `docker-compose -v`.
To be able to run the services. Docker and docker-compose should be installed on the machine. Nvidia-docker is also required if you want to run the services on a GPU (which is default). To install docker, follow the instructions [here](https://docs.docker.com/engine/install/). To install docker-compose, follow the instructions [here](https://docs.docker.com/compose/install/) and to install nvidia-docker, follow the instructions [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker).

## Configuration

The configuration is done in the `.env` file. Users should change the values of the `*_PORT` variables.


## Common Commands

The following commands are common for all the services. The commands are run from the root directory of the repository.

### Start the services

To start the services, run the following command:
```bash
docker-compose up -d
```
### Stop the services
```bash
docker-compose down
```

### Check the status of the services
```bash
docker-compose ps
```

### Check the logs of the services
```bash
docker logs -f
```

### Check the logs of a specific service
```bash
docker logs -f <service-name>
```

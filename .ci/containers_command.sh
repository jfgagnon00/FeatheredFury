#!/bin/bash

DIR=$(dirname "$0")
ENVIRONMENT=$1

shift

# TODO: workaround github action probleme avec .env file
export PYTHON_VERSION="3.9-slim"
export FFURY_APPLICATION_PORT=80
export FFURY_SERVICE_PORT=5001

if [[ "$ENVIRONMENT" == "--azure" ]]
then
    echo "docker-compose pour environment azure"
    export FFURY_PLATFORM="linux/amd64"
    export FFURY_SERVICE_HOST="localhost"
else
    echo "docker-compose pour environment local"
    export FFURY_PLATFORM=""
    export FFURY_SERVICE_HOST="ffury_service" # doit matcher docker-compose.yaml
fi

# echo "'$ENVIRONMENT'"
# echo "'$@'"

docker-compose -f ${DIR}/containers/docker-compose.yaml $@
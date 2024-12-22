#!/bin/bash

# hardcode pour le moment - suppose etre appeler a la racine du projet
docker build --build-arg APPLICATION_PORT=5000 \
             --build-arg SERVICE_PORT=5001 \
             -t application \
             -f .ci/containers/docker-application \
             .

docker build --build-arg SERVICE_PORT=5001 \
             -t service \
             -f .ci/containers/docker-service \
             .
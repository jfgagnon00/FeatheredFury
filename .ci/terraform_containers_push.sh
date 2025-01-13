#!/bin/bash

DIR=$(dirname "$0")

# echo ${FFURY_REGISTRY_SERVER}
# echo ${FFURY_REGISTRY_NAME}

${DIR}/containers_command.sh --azure build

echo "Login Azure ACR"
az acr login --name ${FFURY_REGISTRY_NAME}

echo "Docker tag"
docker tag ffury-web_app:latest ${FFURY_REGISTRY_SERVER}/ffury-web_app:latest
docker tag ffury-web_service:latest ${FFURY_REGISTRY_SERVER}/ffury-web_service:latest

echo "Docker push"
docker push ${FFURY_REGISTRY_SERVER}/ffury-web_app:latest
docker push ${FFURY_REGISTRY_SERVER}/ffury-web_service:latest

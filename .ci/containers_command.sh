#!/bin/bash

DIR=$(dirname "$0")
ENVIRONMENT=$1

shift

if [[ "$ENVIRONMENT" == "--azure" ]]
then
    echo "docker-compose pour environment azure"
    EnvironmentEnvFileOverrides=".env-azure"
else
    echo "docker-compose pour environment local"
    EnvironmentEnvFileOverrides=".env-local"
fi

# echo "'$ENVIRONMENT'"
# echo "'$@'"

env | grep FFURY

ls -la

cd ../ci/containers
echo "docker-compose --env-file ${DIR}/containers/.env --env-file ${DIR}/containers/${EnvironmentEnvFileOverrides} -f ${DIR}/containers/docker-compose.yaml $@"

docker-compose \
    --env-file ${DIR}/containers/.env \
    --env-file ${DIR}/containers/${EnvironmentEnvFileOverrides} \
    -f ${DIR}/containers/docker-compose.yaml $@

docker images
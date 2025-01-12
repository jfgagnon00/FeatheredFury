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

echo '${DIR}'

pwd

echo "docker-compose --env-file ${DIR}/containers/.env --env-file ${DIR}/containers/${EnvironmentEnvFileOverrides} -f ${DIR}/containers/docker-compose.yaml $@"

cd containers

docker-compose --version
docker-compose \
    --env-file ./.env \
    --env-file ./${EnvironmentEnvFileOverrides} \
    -f ./docker-compose.yaml $@

docker images
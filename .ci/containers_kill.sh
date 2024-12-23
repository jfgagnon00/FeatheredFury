#!/bin/bash

docker-compose --env-file .ci/containers/.env  -f .ci/containers/docker-compose.yaml down --volumes --rmi local --remove-orphans
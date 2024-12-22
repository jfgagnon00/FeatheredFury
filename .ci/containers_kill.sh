#!/bin/bash

# hardcode pour le moment - suppose etre appeler a la racine du projet
docker stop $(docker ps -q --filter ancestor=service)
docker stop $(docker ps -q --filter ancestor=application)
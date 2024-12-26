#!/bin/bash

DIR=$(dirname "$0")

${DIR}/containers_command.sh "$1" down --volumes --rmi local --remove-orphans
#!/bin/bash

# script pour gerer l'installation/activation de l'environnement virtuel

PYTHON_INTERPRETER=$1
ENV_NAME=$2

# verifier si deja dans environment
if [[ "$VIRTUAL_ENV" != "" ]]
then
  InVenv=1
else
  InVenv=0
fi

if [ $InVenv -eq 1 ]; then
    echo "Dejà dans un environment python"
    return
fi

# verifier si snake environment existe
NeedInstall=0
if ! [ -f .venv/bin/activate ]; then
    NeedInstall=1
    echo "Création environment pour $ENV_NAME"
    $PYTHON_INTERPRETER -m venv .venv --prompt $ENV_NAME
fi

echo "Activation environment pour $ENV_NAME"
source .venv/bin/activate

if [ $NeedInstall -eq 1 ]; then
    echo "Installation des dépendences"
    $PYTHON_INTERPRETER install --upgrade pip
    $PYTHON_INTERPRETER -m pip install -r requirements.txt
fi
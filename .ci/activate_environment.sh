#!/bin/bash

# script pour gerer l'installation/activation de l'environnement virtuel

SCRIPT="$0"

# si le script est source BASH_SOURCE[0] devrait avoir la source
# sauf sur Mac...
if [[ "${BASH_SOURCE[0]}" != "" && "${BASH_SOURCE[0]}" != "${0}" ]]; then
    SCRIPT="${BASH_SOURCE[0]}"
fi

# resoudre symlinks and obtenir path absolue
SCRIPT_DIR=$(dirname "$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")")
PYTHON_INTERPRETER=$1
ENV_NAME=$2
FORCE_INSTALLATION=$3

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

# verifier si environment existe
NeedInstall=0
if ! [ -f .venv/bin/activate ] && ! [ -f .venv/Scripts/activate ]; then
    NeedInstall=1
    echo "Création environment pour $ENV_NAME"
    $PYTHON_INTERPRETER -m venv .venv --prompt $ENV_NAME
fi

if [[ $NeedInstall -eq 0 && "$FORCE_INSTALLATION" == "--force" ]]
then
    NeedInstall=1
    echo "Forcer réinstallation pour $ENV_NAME"
else
    echo "Activation environment pour $ENV_NAME"
fi

# difference entre windows et linux/mac
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
else
    source .venv/Scripts/activate
fi

if [ $NeedInstall -eq 1 ]; then
    echo "Installation des dépendences"

    $PYTHON_INTERPRETER -m pip install --upgrade pip
    $PYTHON_INTERPRETER -m pip install -r "${SCRIPT_DIR}/requirements-local.txt"

    # s'assurer que les jupyter notebook pointent aussi sur bon environment
    $PYTHON_INTERPRETER -m ipykernel install --user --name $ENV_NAME --display-name $ENV_NAME
fi
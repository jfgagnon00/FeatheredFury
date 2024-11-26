#!/bin/bash

# script pour gerer l'installation/activation de l'environnement virtuel

# Function to get the absolute path of the current script
get_script_path() {
    # In case the script is sourced or executed directly
    local script="$0"

    # If the script is sourced (i.e., BASH_SOURCE[0] will hold the source path)
    if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
        script="${BASH_SOURCE[0]}"
    fi

    # Resolve symlinks and get the absolute path
    local script_dir
    script_dir=$(dirname "$(readlink -f "$script" 2>/dev/null || echo "$script")")

    echo "$script_dir"
}

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
if ! [ -f .venv/bin/activate ]; then
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

source .venv/bin/activate

if [ $NeedInstall -eq 1 ]; then
    echo "Installation des dépendences"

    $PYTHON_INTERPRETER -m pip install --upgrade pip
    $PYTHON_INTERPRETER -m pip install -r "$(get_script_path)/requirements-local.txt"

    # s'assurer que les jupyter notebook pointent aussi sur bon environment
    $PYTHON_INTERPRETER -m ipykernel install --user --name $ENV_NAME --display-name $ENV_NAME
fi
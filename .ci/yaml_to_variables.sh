#!/bin/bash

# script pour convertir variables d'un fichier .yaml en variable bash

YAML_TO_READ=$1
DEBUG_OUTPUT=$2

# verifier si deja dans environment
if [[ "$DEBUG_OUTPUT" == "--debug" ]]
then
    DebugOutput=1
else
    DebugOutput=0
fi

# enlever commentaires du yaml
vars=$(sed '/!ffury/d' ${YAML_TO_READ} | yq '... comments=""')

# format de l'output:
# NOM_DE_VARIABLE: VALEUR_DE_VARIABLE
IFS=": "

while read -r key_value_pair; do
    # separer key de valeur
    read -ra kv <<< $key_value_pair

    key=${kv[0]}

    if [ "${kv[1]}" == "!relative_path" ]; then
        path="$(dirname "${YAML_TO_READ}")"
        path="$(realpath -q "${path}")"
        value="${path}/${kv[2]}"
    else
        value="${kv[1]}"
    fi

    if [ $DebugOutput -eq 1 ]; then
        # test, afficher resultat sans les appliquer
        echo "${key}=${value}"
    else
        # ajouter aux variables de script
        declare ${key}="${value}"
    fi
done <<< $vars

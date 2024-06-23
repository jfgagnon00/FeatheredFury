#!/bin/bash

# script pour convertir variables d'un fichier .yaml en variable bash

YAML_TO_READ=$1

# enlever commentaires du yaml
vars=$(yq '... comments=""' ${YAML_TO_READ})

# format de l'output:
# NOM_DE_VARIABLE: VALEUR_DE_VARIABLE
IFS=": "

while read -r key_value_pair; do
    # separer key de valeur
    read -ra kv <<< $key_value_pair

    # ajouter aux variables de script
    declare ${kv[0]}="${kv[1]}"
done <<< $vars

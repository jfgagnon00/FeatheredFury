"""
Module encapsulant yaml. Ajoute fonctionalites 
rudimentaire pour deserializer et quelques tags.

Voir YamlDeserializable et YamlTag pour etendre 
cette fonctinalite.

Tags supportes (voir plus bas pour details):
    !include
    !relative_path
"""

import yaml

from pathlib import Path
from .yaml_decorators import YamlDeserializable, YamlTag

def _resolve_relative_path(loader, node):
    base_path = Path(loader.stream.name).parent
    filename = loader.construct_scalar(node)
    return Path.joinpath(base_path, filename).resolve()

@YamlTag("!include")
def _yaml_include_deserialize(loader, node):
    """
    La valeur d'une propriete yaml sera etablie en
    deserialisant le fichier reference par !include. 
    Le path du fichier est relatif au fichier yaml 
    qui le contient.
    """
    filename = _resolve_relative_path(loader, node)
    with open(filename, "r") as f:
        return yaml.load(f, Loader=yaml.Loader)

@YamlTag("!relative_path")
def _yaml_relative_path_deserialize(loader, node):
    """
    La valeur d'une propriete yaml sera etablie en
    convertissant le nom fichier reference par !relative_path
    en sa valeur absolue. Le path du fichier est 
    relatif au fichier yaml qui le contient.

    Ex) 
        data_dir: !relative_path ./data
        data_dir => /Users/auser/project/dataset/data
    """
    return _resolve_relative_path(loader, node)

def load_yaml(filename):
    """
    Load un fichier yaml
    """
    with open(filename, "r") as f:
        return yaml.load(f, Loader=yaml.Loader)

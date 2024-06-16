import yaml

from .MetaObject import MetaObject

from pathlib import Path

# ajout mot clef aux fichiers .yaml
# pour inclure d'autres fichiers .yaml
_YAML_INCLUDE_KEYWORD = "!include"

def _yaml_include_parse(loader, node):
    # include path relatif au fichier .yaml lui meme
    filename = Path.joinpath(Path(loader.name).parent, Path(node.value))

    # processer l'include
    return MetaObject.from_yaml(filename)

if not _YAML_INCLUDE_KEYWORD in yaml.Loader.yaml_constructors:
    # enregistrer le nouveau mot clef s'il n'est pas present
    yaml.add_constructor(_YAML_INCLUDE_KEYWORD, _yaml_include_parse)

def create_config(filename):
    """
    Creee une configuration a partir d'un fichier
    """
    return MetaObject.from_yaml(filename)

def override_config(instance, object):
    """
    Override attributs de instance avec les valeurs 
    lues a fichier de filename
    """
    MetaObject.override_from_object(instance, object)

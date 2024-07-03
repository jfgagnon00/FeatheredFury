import yaml

from pathlib import Path
from .MetaObject import MetaObject

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

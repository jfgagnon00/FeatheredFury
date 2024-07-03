import yaml

from pathlib import Path

# ajout mot clef aux fichiers .yaml
# pour inclure path relatif au .yaml courant
_YAML_RELATIVE_PATH_KEYWORD = "!relative_path"

def _yaml_relative_path_parse(loader, node):
    # path relatif au fichier .yaml lui meme
    path = Path.joinpath(Path(loader.name).parent, Path(node.value))
    return str(path.resolve())

if not _YAML_RELATIVE_PATH_KEYWORD in yaml.Loader.yaml_constructors:
    # enregistrer le nouveau mot clef s'il n'est pas present
    yaml.add_constructor(_YAML_RELATIVE_PATH_KEYWORD, _yaml_relative_path_parse)

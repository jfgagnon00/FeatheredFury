import ffury

from ..yaml import load_yaml

from .ProjectConfig import ProjectConfig
from .PathsConfig import PathsConfig
from .BirdClefConfig import BirdClefConfig


# nom fichier config par defaut 
DEFAULT_CONFIG_FILE = f"{ffury.__name__}.yaml"

def load_config(filename=DEFAULT_CONFIG_FILE):
    """
    Load une configuration a partir d'un fichier
    """
    return load_yaml(filename)

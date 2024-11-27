import ffury

from ..yaml import load_yaml

from .ProjectConfig import (
    DatasetType,
    ProjectConfig
)
from .PathsConfig import PathsConfig
from .BirdClefConfig import BirdClefConfig
from .PreprocessConfig import PreprocessConfig
from .TrainConfig import TrainConfig
from .TrainParameters import TrainParameters


# nom fichier config par defaut 
DEFAULT_CONFIG_FILE = f"{ffury.__name__}.yaml"

def load_config(filename : str = DEFAULT_CONFIG_FILE) -> ProjectConfig:
    """
    Load une configuration a partir d'un fichier
    """
    return load_yaml(filename)

import ffury

from .ApplicationConfig import ApplicationConfig
from .BirdClefConfig import BirdClefConfig
from .PathsConfig import PathsConfig
from .PreprocessConfig import PreprocessConfig
from .ProjectConfig import (
    DatasetType,
    ProjectConfig
)
from .ServiceConfig import ServiceConfig
from .TrainConfig import TrainConfig
from .TrainParameters import TrainParameters

from ..yaml import load_yaml


# nom fichier config par defaut 
DEFAULT_CONFIG_FILE = f"{ffury.__name__}.yaml"

def load_config(filename : str = DEFAULT_CONFIG_FILE) -> ProjectConfig:
    """
    Load une configuration a partir d'un fichier
    """
    # TODO: 
    # 1. decorateur yaml demande de connaitre tous les 
    # types avant de loader un fichier qui peut les utiliser
    # a refactorer
    # 2. Avec package optionel, le reload des configs est a revoir
    from ..optional.development.keras_adapters import (
        KerasDummyModelFactory,
        KerasTrainable
    )

    return load_yaml(filename)

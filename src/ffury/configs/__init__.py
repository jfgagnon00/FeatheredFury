import ffury

from .ApplicationConfig import ApplicationConfig
from .AzureConfig import AzureConfig
from .BirdClefConfig import BirdClefConfig
from .EvidentlyConfig import EvidentlyConfig
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
    try:
        # TODO: 
        # decorateur yaml demande de connaitre tous les 
        # types avant de loader un fichier qui peut les utiliser
        # a refactorer
        from ..optional.development.keras_adapters import (
            KerasDummyModelFactory,
            KerasTrainable
        )
    except ImportError:
        pass

    return load_yaml(filename)

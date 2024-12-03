from enum import (
    auto,
    IntEnum
)
from pathlib import Path

from ..yaml import YamlDeserializable

from .PathsConfig import PathsConfig
from .BirdClefConfig import BirdClefConfig
from .PreprocessConfig import PreprocessConfig
from .TrainConfig import TrainConfig


class DatasetType(IntEnum):
    TRAIN = auto()
    TEST = auto()
    VALIDATION = auto()
    RAW = auto()
    EXPLORED = auto()
    PREPROCESS = auto()

    # a usage interne
    _SPECIES = auto()

    @property
    def _csv_filename(self):
        return f"data_{self.name_lowercase}.csv" 

    @property
    def _hdf5_filename(self):
        return f"data_{self.name_lowercase}.hdf5" 

    @property
    def name_lowercase(self):
        return self.name.lower()

@YamlDeserializable
class ProjectConfig:
    """
    Configurations globales
    """
    def __init__(self):
        self.num_classes = 0
        self.paths = PathsConfig()
        self.dataset = BirdClefConfig()
        self.preprocess = PreprocessConfig()
        self.train = TrainConfig()

        # configs interne
        self._ulimit_workaround = 2048

    def get_audio_filename(self, filename: str) -> str:
        """
        Commodite pour composer le chemin complet pour avoir un ficheir audio
        """
        path = Path.joinpath(self.paths.DATA_RAW_DIR,
                             self.dataset.audio_dir, 
                             filename)
        return str(path.resolve())
    
    def get_csv_filename(self, 
                         type_: DatasetType) -> str:
        """
        Obtenir le chemin complet pour un dataset en format csv (source)
        """
        if type_ == DatasetType.RAW:
            folder = self.paths.DATA_RAW_DIR
            filename = self.dataset.csv_filename
        else:
            folder = self.paths.DATA_DIR
            filename = type_._csv_filename

        path = Path.joinpath(folder, filename)
        return str(path.resolve())
    
    def get_hdf5_filename(self,
                          type_: DatasetType) -> str:
        """
        Obtenir le chemin complet pour un dataset en format hdf5 (preprocesse)
        """
        if type_ == DatasetType.RAW or \
           type_ == DatasetType.EXPLORED:
            raise ValueError(f"{type_.name} n'est pas supporte en format hdf5")

        path = Path.joinpath(self.paths.BUILD_DIR, 
                             type_._hdf5_filename)
        return str(path.resolve())

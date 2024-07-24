from pathlib import Path

from ..yaml import YamlDeserializable

from .PathsConfig import PathsConfig
from .BirdClefConfig import BirdClefConfig
from .PreprocessConfig import PreprocessConfig


@YamlDeserializable
class ProjectConfig:
    """
    Configurations globales
    """
    def __init__(self):
        self.paths = PathsConfig()
        self.dataset = BirdClefConfig()
        self.preprocess = PreprocessConfig()

    def get_audio_filename(self, filename: str) -> str:
        """
        Commodite pour composer le chemin complet pour avoir un ficheir audio
        """
        path = Path.joinpath(self.paths.DATA_RAW_DIR,
                             self.dataset.audio_dir, 
                             filename)
        return str(path.resolve())
    
    def get_dataset_raw_filename(self) -> str:
        """
        Utilitaire pour loader dataset raw
        """
        path = Path.joinpath(self.paths.DATA_RAW_DIR, 
                             self.dataset.csv_filename)
        return str(path.resolve())

    def get_dataset_explored_filename(self) -> str:
        """
        Utilitaire pour loader dataset raw
        """
        path = Path.joinpath(self.paths.DATA_DIR, 
                             "data_explored.csv")
        return str(path.resolve())

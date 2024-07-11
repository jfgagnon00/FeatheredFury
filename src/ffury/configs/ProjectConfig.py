from pathlib import PurePath

from ..yaml import YamlDeserializable

from .PathsConfig import PathsConfig
from .BirdClefConfig import BirdClefConfig


@YamlDeserializable
class ProjectConfig:
    """
    Configurations globales
    """
    def __init__(self):
        self.paths = PathsConfig()
        self.dataset = BirdClefConfig()

    def get_audio_filename(self, filename):
        """
        Commodite pour composer le chemin complet pour avoir un ficheir audio
        """
        return PurePath.joinpath(self.paths.DATA_RAW_DIR,
                                 self.dataset.audio_dir, 
                                 filename)
    
    def get_dataset_raw_filename(self):
        """
        Utilitaire pour loader dataset raw
        """
        return PurePath.joinpath(self.paths.DATA_RAW_DIR, 
                                 self.dataset.csv_filename)

from pathlib import Path

from .MetaObject import MetaObject

class ProjectConfig(MetaObject):
    """
    Encapsule les proprietes globales au projet
    """
    def __init__(self):
        self.PROJECT_NAME = ""
        self.PYTHON_INTERPRETER = ""
        self.CONFIGS_DIR = ""
        self.BUILD_DIR = ""
        self.DATA_DIR = ""
        self.MODELS_DIR = ""
        self.CI_DIR = ""

    @property
    def dataRawDir(self):
        "Utilitaire pour avoir data/raw"
        return Path(self.DATA_DIR).joinpath("raw")

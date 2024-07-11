from pathlib import PurePath
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class PathsConfig:
    """
    Encapsule les proprietes pour les paths
    """
    def __init__(self):
        # garder en majuscule car ses attributs sont
        # aussi refletes par des variables d'environments
        # garde la syntaxe entre python, yaml et bash scripts
        # uniforme
        self.PROJECT_NAME = ""
        self.PYTHON_INTERPRETER = ""
        self.CONFIGS_DIR = ""
        self.BUILD_DIR = ""
        self.DATA_DIR = ""
        self.MODELS_DIR = ""
        self.CI_DIR = ""

    @property
    def DATA_RAW_DIR(self):
        "Commodite pour avoir data/raw"
        return PurePath(self.DATA_DIR).joinpath("raw")

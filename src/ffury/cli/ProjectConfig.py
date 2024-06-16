from ..configs import MetaObject

class ProjectConfig(MetaObject):
    """
    Encapsule les proprietes globales au projet
    """
    def __init__(self):
        self.PROJECT_NAME = "FeatheredFury"
        self.PYTHON_INTERPRETER = ""
        self.CONFIGS_DIR = "configs"
        self.BUILD_DIR = "build"
        self.DATA_DIR = "data"
        self.MODELS_DIR = "models"
        self.CI_DIR = ".ci"

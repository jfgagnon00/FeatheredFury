# ajout yaml include extension
import ffury.configs._yaml_include_extension

from .KaggleConfig import KaggleConfig
from .MetaObject import MetaObject
from .ProjectConfig import ProjectConfig


# nom fichier config par defaut 
DEFAULT_CONFIG_FILE = "ffury_configs.yaml"

def load_config(filename):
    """
    Load une configuration a partir d'un fichier
    """
    return MetaObject.from_yaml(filename)

def override_config(instance, object):
    """
    Override attributs de instance avec les valeurs 
    lues a fichier de filename
    """
    MetaObject.override_from_object(instance, object)

def create_config(filename=DEFAULT_CONFIG_FILE):
    # configurations par defaut
    project = ProjectConfig()
    dataset = KaggleConfig()

    # creation des overrides
    configOverrides = load_config(filename)

    if not configOverrides is None:
        # appliquer overrides sur configiguration par defaut
        override_config(project, configOverrides.project)
        override_config(dataset, configOverrides.dataset)

    return MetaObject.from_kwargs(project=project,
                                  dataset=dataset)

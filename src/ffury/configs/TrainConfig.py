from ..misc.IFactory import IFactory
from ..misc.IMeasurable import IMeasurable
from ..misc.ITrainable import ITrainable
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class TrainConfig:
    """
    Encapsule les proprietes pour le training
    """
    def __init__(self):
        self.model_factory = None
        self.measurable = None
        self.trainable = None
        self.parameters = None

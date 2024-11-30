from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class TrainConfig:
    """
    Encapsule les proprietes pour le training
    """
    def __init__(self):
        self.model_factory = None
        self.metrics = None
        self.trainer = None
        self.parameters = None

from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class TrainParameters:
    """
    Encapsule les parametres pour le training
    (tout ce qui est independant du trainer)
    """
    def __init__(self):
        self.learning_rate = 0
        self.epochs = 0
        self.batch_size = 0

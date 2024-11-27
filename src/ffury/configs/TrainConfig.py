from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class TrainConfig:
    """
    Encapsule les proprietes pour le training
    """
    def __init__(self):
        self.model = None
        self.trainer = None
        self.learning_rate = 0
        self.epoch = 0
        self.batch_size = 0
        self.test_every_n_steps = 1

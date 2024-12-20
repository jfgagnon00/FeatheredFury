from ..yaml import YamlDeserializable


@YamlDeserializable
class ApplicationConfig:
    """
    Encapsule les proprietes de l'application flask
    """
    def __init__(self):
        self.port = 5000
        self.host = "0.0.0.0"

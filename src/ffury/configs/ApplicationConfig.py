from ..yaml import YamlDeserializable


@YamlDeserializable
class ApplicationConfig:
    """
    Encapsule les proprietes de l'application flask
    """
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 80

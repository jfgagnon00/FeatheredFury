from ..yaml import YamlDeserializable


@YamlDeserializable
class ServiceConfig:
    """
    Encapsule les proprietes du service flask
    """
    def __init__(self):
        self.port = 5001

        # pour qu'une application dans un conteneur soit accessible 
        # depuis l"extérieur, elle doit écouter sur 0.0.0.0 et non 127.0.0.1
        self.host = "0.0.0.0"

        self.protocol = "http"

        self.max_content_size = 4 * 1024 * 1024
        self.allowed_extensions = (".wav", ".mp3", ".ogg")

    @property
    def _base_url(self):
        return f"{self.protocol}://{self.host}:{self.port}/api"

    @property
    def predict_url(self):
        return f"{self._base_url}/predict"

    @property
    def validation_url(self):
        return f"{self._base_url}/validation"

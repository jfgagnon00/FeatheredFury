from ..yaml import YamlDeserializable


@YamlDeserializable
class ServiceConfig:
    """
    Encapsule les proprietes du service flask
    """
    def __init__(self):
        self.port = 5001

        # todo Pour qu"une application dans un conteneur soit accessible depuis l"extérieur, elle doit écouter sur 0.0.0.0 et non 127.0.0.1
        self.host = "0.0.0.0"

        self.protocol = "http"

    @property
    def _base_url(self):
        # api : nom du conteneur
        return f"{self.protocol}://{self.host}:{self.port}/api"

    @property
    def waveform_url(self):
        return f"{self._base_url}/waveform"

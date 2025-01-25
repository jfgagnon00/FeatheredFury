from ..misc.environment_variable import getenv
from ..yaml import YamlDeserializable


@YamlDeserializable
class EvidentlyConfig:
    """
    Encapsule les proprietes relative aux tests pour Evidently
    """
    def __init__(self):
        self.threshold = 0
        self.quantile_probability = 0
        self.pca_components = None

    @property
    def api_token(self) -> str:
        return getenv("EVIDENTLY_API_TOKEN")

    @property
    def project_id(self) -> str:
        return getenv("EVIDENTLY_PROJECT_ID")
    
    @property
    def url(self) -> str:
        return "https://app.evidently.cloud"

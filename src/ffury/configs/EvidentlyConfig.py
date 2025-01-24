import os

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

        self.url = "https://app.evidently.cloud"
        self.api_token = EvidentlyConfig._getenv("EVIDENTLY_API_TOKEN")
        self.project_id = EvidentlyConfig._getenv("EVIDENTLY_PROJECT_ID")

    @staticmethod
    def _getenv(var_name):
        value = os.getenv(var_name)
        if value is None or value == "":
            print(f"{var_name} non definie")
        return value

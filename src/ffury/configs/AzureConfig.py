from ..misc.environment_variable import getenv
from ..yaml import YamlDeserializable


@YamlDeserializable
class AzureConfig:
    """
    Encapsule les proprietes relative a Azure
    """
    def __init__(self):
        pass

    @property
    def conn_str(self) -> str:
        return getenv("AZURE_STORAGE_CONNECTION_STRING")

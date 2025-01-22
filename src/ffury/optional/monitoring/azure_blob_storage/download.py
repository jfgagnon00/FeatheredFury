from azure.storage.blob import BlobServiceClient
from typing import (
    Any,
    Tuple
)


from .properties import _TIMESTAMP
from .client_service import get_client_service


def download(container_name: str,
             blob_name: str) -> Tuple[Any, float]:
    with get_client_service() as client_service:
        with client_service.get_blob_client(container=container_name, 
                                            blob=blob_name) as blob_client:
            data = blob_client.download_blob().readall()
            metadata = blob_client.get_blob_properties().metadata
            return data, float(metadata[_TIMESTAMP])

def download_file(container_name: str,
                  blob_name: str,
                  filename: str) -> float:
    """
    Download un fichier. AZURE_STORAGE_CONNECTION_STRING doit etre defini.
    """
    data, timestamp = download(container_name, blob_name)
    with open(filename, "wb") as file:
        file.write(data)
    return timestamp

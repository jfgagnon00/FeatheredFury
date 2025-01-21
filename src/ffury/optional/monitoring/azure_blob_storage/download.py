import os

from azure.storage.blob import BlobServiceClient
from typing import (
    Any,
    Tuple
)

from .properties import _TIMESTAMP


def download(container_name: str,
             blob_name: str) -> Tuple[Any, float]:
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    with BlobServiceClient.from_connection_string(conn_str=conn_str) as client_service:
        with client_service.get_blob_client(container=container_name, 
                                            blob=blob_name) as blob_client:
            data = blob_client.download_blob().readall()
            metadata = blob_client.get_blob_properties().metadata
            return data, float(metadata[_TIMESTAMP])

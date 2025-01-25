from azure.storage.blob import BlobServiceClient
from ffury.configs import AzureConfig
from typing import (
    Any,
    Tuple
)


from .properties import _TIMESTAMP


def download(container_name: str,
             blob_name: str,
             config: AzureConfig) -> Tuple[Any, float]:
    with BlobServiceClient.from_connection_string(conn_str=config.conn_str) as client_service:
        with client_service.get_blob_client(container=container_name, 
                                            blob=blob_name) as blob_client:
            data = blob_client.download_blob().readall()
            metadata = blob_client.get_blob_properties().metadata
            return data, float(metadata[_TIMESTAMP])

def download_file(container_name: str,
                  blob_name: str,
                  filename: str,
                  config: AzureConfig) -> float:
    data, timestamp = download(container_name, 
                               blob_name,
                               config)
    with open(filename, "wb") as file:
        file.write(data)
    return timestamp

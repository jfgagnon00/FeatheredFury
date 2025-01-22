import os

from azure.storage.blob import BlobServiceClient
from ffury.misc.logging import create_logger
from typing import Any

from .properties import _TIMESTAMP


def upload(container_name: str,
           blob_name: str,
           blob_data: Any,
           timestamp: float) -> None:
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    with BlobServiceClient.from_connection_string(conn_str=conn_str) as client_service:
        container_client = client_service.get_container_client(container_name)
        if container_client is None or not container_client.exists():
            logger = create_logger(file=__file__)
            logger.info(f"Creation container {container_name}")
            container_client = client_service.create_container(container_name)
        with container_client.upload_blob(name=blob_name, 
                                          data=blob_data,
                                          overwrite=True) as blob_client:
            metadata = blob_client.get_blob_properties().metadata
            metadata.update({_TIMESTAMP: str(timestamp)})
            blob_client.set_blob_metadata(metadata)

def upload_file(filename: str,
                container_name: str,
                blob_name: str,
                timestamp: float) -> None:
    """
    Upload un fichier. AZURE_STORAGE_CONNECTION_STRING doit etre defini.
    """
    with open(filename, "rb") as file:
        upload(container_name,
               blob_name,
               file,
               timestamp)

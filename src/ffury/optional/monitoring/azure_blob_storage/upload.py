from ffury.misc.logging import create_logger
from typing import Any


from .client_service import get_client_service
from .properties import _TIMESTAMP


def upload(container_name: str,
           blob_name: str,
           blob_data: Any,
           timestamp: float) -> None:
    metadata = {_TIMESTAMP: str(timestamp)}
    with get_client_service() as client_service:
        container_client = client_service.get_container_client(container_name)
        if container_client is None or not container_client.exists():
            logger = create_logger(file=__file__)
            logger.info(f"Creation container {container_name}")
            container_client = client_service.create_container(container_name)
        metadata_ = container_client.get_container_properties().metadata
        metadata_.update(metadata)
        container_client.set_container_metadata(metadata_)
        with container_client.upload_blob(name=blob_name, 
                                          data=blob_data,
                                          overwrite=True) as blob_client:
            metadata_ = blob_client.get_blob_properties().metadata
            metadata_.update(metadata)
            blob_client.set_blob_metadata(metadata_)

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

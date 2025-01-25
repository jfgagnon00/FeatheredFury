from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient
)
from ffury.configs import AzureConfig
from typing import Iterator


from .properties import _TIMESTAMP


def get_containers(name_starts_with: str,
                   timestamp_lo: float,
                   timestamp_high: float,
                   config: AzureConfig) -> Iterator[ContainerClient]:
    with BlobServiceClient.from_connection_string(conn_str=config.conn_str) as client_service:
        for c in client_service.list_containers(name_starts_with, include_metadata=True):
            ts = float(c.metadata[_TIMESTAMP])
            if timestamp_lo <= ts and ts <= timestamp_high:
                yield client_service.get_container_client(c.name)

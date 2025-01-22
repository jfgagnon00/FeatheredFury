from azure.storage.blob import ContainerClient
from typing import Iterator


from .properties import _TIMESTAMP
from .client_service import get_client_service


def get_containers(name_starts_with: str,
                   timestamp_lo: float,
                   timestamp_high: float,) -> Iterator[ContainerClient]:
    with get_client_service() as client_service:
        for c in client_service.list_containers(name_starts_with, include_metadata=True):
            ts = float(c.metadata[_TIMESTAMP])
            if timestamp_lo <= ts and ts <= timestamp_high:
                yield client_service.get_container_client(c.name)

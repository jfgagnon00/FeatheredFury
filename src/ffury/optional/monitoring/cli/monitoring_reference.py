import click

from pathlib import Path

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig

from ffury.misc.logging import create_logger


from .monitoring import monitoring_group
from ..azure_blob_storage.properties import (
    _REFERENCE_BLOB,
    _REFERENCE_CONTAINER
)
from ..azure_blob_storage import (
    download,
    upload
)
from ..misc.timestamp import (
    date_from_timestamp,
    timestamp_now
)


@monitoring_group.command()
@ProjectConfigDecorator
def upload_reference(project_config: ProjectConfig) -> None:
    """
    Upload les features de reference pour traitement ulterieur.
    AZURE_STORAGE_CONNECTION_STRING doit etre defini.
    """
    logger = create_logger(file=__file__)
    logger.info("Upload reference features")
    with open(_get_filename(project_config), "rb") as file:
        ts = timestamp_now()
        upload(_REFERENCE_CONTAINER,
               _REFERENCE_BLOB,
               file,
               ts)
    logger.info(f"Uploaded reference features timestamp: { date_from_timestamp(ts) }")

@monitoring_group.command()
@ProjectConfigDecorator
def download_reference(project_config: ProjectConfig) -> None:
    """
    Download les features de reference pour traitement ulterieur.
    AZURE_STORAGE_CONNECTION_STRING doit etre defini.
    """
    logger = create_logger(file=__file__)
    logger.info("Download reference features")
    data, timestamp = download(_REFERENCE_CONTAINER, _REFERENCE_BLOB)
    with open(_get_filename(project_config), "wb") as file:
        file.write(data)
    logger.info(f"Downloaded reference features timestamp: { date_from_timestamp(timestamp) }")

def _get_filename(project_config: ProjectConfig) -> str:
    return Path.joinpath(project_config.paths.BUILD_DIR, "monitoring_features.csv")

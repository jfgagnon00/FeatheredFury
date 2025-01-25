import click

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig

from ffury.misc.logging import create_logger


from .monitoring import monitoring_group
from ..azure_blob_storage import (
    download_file,
    upload_file
)
from ..azure_blob_storage.properties import (
    _REFERENCE_BLOB,
    _REFERENCE_CONTAINER,
)
from ..misc.reference import get_filename
from ..misc.timestamp import (
    date_from_timestamp,
    timestamp_now
)


@monitoring_group.command()
@ProjectConfigDecorator
def upload_reference(project_config: ProjectConfig) -> None:
    """
    Upload les features de reference pour traitement ulterieur.
    """
    logger = create_logger(file=__file__)
    logger.info("Upload reference features")
    ts = timestamp_now()
    upload_file(get_filename(project_config),
                _REFERENCE_CONTAINER,
                _REFERENCE_BLOB,
                ts,
                project_config.azure)
    logger.info(f"Uploaded reference features timestamp: { date_from_timestamp(ts) }")

@monitoring_group.command()
@ProjectConfigDecorator
def download_reference(project_config: ProjectConfig) -> None:
    """
    Download les features de reference pour traitement ulterieur.
    """
    logger = create_logger(file=__file__)
    logger.info("Download reference features")
    ts = download_file(_REFERENCE_CONTAINER,
                       _REFERENCE_BLOB,
                       get_filename(project_config),
                       project_config.azure)
    logger.info(f"Downloaded reference features timestamp: { date_from_timestamp(ts) }")

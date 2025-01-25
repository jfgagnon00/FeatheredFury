import click

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig
from ffury.misc.logging import create_logger
from io import StringIO
from pandas import (
    concat,
    read_csv
)

from .monitoring import monitoring_group
from ..azure_blob_storage import (
    download_file,
    get_containers,
    FEATURES_BLOB
)
from ..azure_blob_storage.properties import (
    _REFERENCE_BLOB,
    _REFERENCE_CONTAINER,
)
from ..evidently.embeddings_drift import test_embeddings_drift
from ..misc.reference import get_filename
from ..misc.timestamp import (
    date_from_timestamp,
    timestamp_now_timedelta,
)


@monitoring_group.command()
@ProjectConfigDecorator
def drift_test(project_config: ProjectConfig) -> None:
    """
    Effectue un test de drift sur la distribution des features references. Prend 
    les predictions des derniers 24h.
    """
    logger = create_logger(file=__file__)

    yesterday, today = timestamp_now_timedelta(days=1)
    logger.info(f"Test [{date_from_timestamp(yesterday)}, {date_from_timestamp(today)}]")

    predictions_features_df = None
    for container in get_containers("p", 
                                    yesterday, 
                                    today,
                                    project_config.azure):
        logger.info(f"Obtenir features de {container.container_name}")
        blob_client = container.get_blob_client(FEATURES_BLOB)
        bytes = blob_client.download_blob().readall()
        buffer = StringIO(bytes.decode("UTF-8"))
        features_df = read_csv(buffer)
        if predictions_features_df is None:
            predictions_features_df = features_df
        else:
            predictions_features_df = concat([predictions_features_df, features_df], 
                                              axis=0, 
                                              ignore_index=True)
    if predictions_features_df is None or len(predictions_features_df) == 0:
        raise ValueError("Aucune prediction disponible")

    logger.info("Download features reference")
    filename = get_filename(project_config)
    download_file(_REFERENCE_CONTAINER, 
                  _REFERENCE_BLOB, 
                  filename,
                  project_config.azure)
    reference_features_df = read_csv(filename)
    if reference_features_df is None or len(reference_features_df) == 0:
        raise ValueError("Aucune referencer disponible")

    success = test_embeddings_drift(reference_features_df,
                                    predictions_features_df,
                                    project_config.evidently)

    exit( 0 if success else -1 )

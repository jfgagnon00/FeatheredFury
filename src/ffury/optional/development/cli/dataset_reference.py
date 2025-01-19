import click
import numpy as np

from pandas import DataFrame
from pathlib import Path

from ffury.cli import ProjectConfigDecorator
from ffury.configs import (
    DatasetType,
    PathsConfig,
    ProjectConfig
)

from ffury.misc.logging import create_logger
from ffury.optional.keras_adapters import _load_model


from .dataset import dataset_group
from ..dataset.IndexedDataset import IndexedDataset
from ..misc.ulimit import ulimit_workaround


@dataset_group.command()
@ProjectConfigDecorator
def reference(project_config: ProjectConfig) -> None:
    """
    Genere les features de reference a partir du data indexe train et du modele
    """
    # TODO: a enlever
    ulimit_workaround(project_config)

    logger = create_logger(file=__file__)

    model = _load_model(project_config)
    dataset = IndexedDataset.create(project_config, DatasetType.TRAIN)

    logger.info("Extraction features")
    _, group_features = model.predict(dataset.spectrogram_groups)

    print(group_features.shape)
    group_features = np.mean(group_features, axis=1)
    print(group_features.shape)

    logger.info("Sauvegarde features")
    features_df = DataFrame(data=group_features,
                            columns=[f"feat_{i}" for i in range(group_features.shape[-1])])

    filename = Path.joinpath(project_config.paths.BUILD_DIR, "monitoring_features.csv")
    features_df.to_csv(filename, index=False)

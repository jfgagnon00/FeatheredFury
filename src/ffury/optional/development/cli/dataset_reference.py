import click

from pathlib import Path
from tqdm import tqdm

from ffury.cli import ProjectConfigDecorator
from ffury.configs import (
    DatasetType,
    ProjectConfig
)

from ffury.misc.logging import create_logger

from typing import Any

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

    for i in tqdm( range(dataset.spectrogram_groups.shape[0]) ):
        pass

def _load_model(project_config: ProjectConfig) -> Any:
    filename = Path.joinpath(project_config.paths.MODELS_DIR, "Model.keras")
    if Path.is_file(filename):
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from keras.models import load_model
        return load_model(filename)
    else:
        raise ValueError(f"{filename} n'existe pas")
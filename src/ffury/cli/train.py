import click

from . import ProjectConfigDecorator
    
from ..configs import (
    DatasetType,
    ProjectConfig
)
from ..dataset import IndexedDataset
from ..misc.IFactory import IFactory


@click.command()
@ProjectConfigDecorator
def train(project_config: ProjectConfig) -> None:
    """
    Encapsule l'entrainement
    """
    train_config = project_config.train

    if not isinstance(train_config.model_factory, IFactory):
        raise ValueError(f"{type(train_config.model_factory)} n'implemente pas IFactory")
    model = train_config.model_factory.create_from_config(project_config)

    train = IndexedDataset(project_config, DatasetType.TRAIN)
    validation = IndexedDataset(project_config, DatasetType.VALIDATION)

    train_config.trainer(project_config.paths,
                         train_config.parameters,
                         train_config.metrics,
                         model,
                         train.spectrogram_groups, train.y,
                         validation.spectrogram_groups, validation.y)

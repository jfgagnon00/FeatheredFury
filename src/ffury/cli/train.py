import click

from . import ProjectConfigDecorator
from ..configs import (
    DatasetType,
    ProjectConfig
)
from ..dataset import IndexedDataset
from ..trainers import *

@click.command()
@ProjectConfigDecorator
def train(project_config: ProjectConfig):
    """
    Encapsule l'entrainement
    """
    train = IndexedDataset(project_config, 
                           DatasetType.TRAIN)

    validation = IndexedDataset(project_config, 
                                DatasetType.VALIDATION)
 
    project_config.train.trainer(project_config.paths,
                                 project_config.train.parameters,
                                 project_config.train.metrics,
                                 project_config.train.model,
                                 train.spectrogram_groups, train.y,
                                 validation.spectrogram_groups, validation.y)

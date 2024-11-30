import click

from . import ProjectConfigDecorator
    
from ..configs import (
    DatasetType,
    ProjectConfig
)
from ..dataset import IndexedDataset

@click.command()
@ProjectConfigDecorator
def train(project_config: ProjectConfig) -> None:
    """
    Encapsule l'entrainement
    """
    if not hasattr(project_config.train.model_factory, "create_from_config"):
        raise ValueError(f"{type(project_config.train.model_factory)} n'a pas la methode 'create_from_config'")

    model = project_config.train.model_factory.create_from_config(project_config)

    train = IndexedDataset(project_config, 
                        DatasetType.TRAIN)

    validation = IndexedDataset(project_config, 
                                DatasetType.VALIDATION)

    project_config.train.trainer(project_config.paths,
                                project_config.train.parameters,
                                project_config.train.metrics,
                                model,
                                train.spectrogram_groups, train.y,
                                validation.spectrogram_groups, validation.y)

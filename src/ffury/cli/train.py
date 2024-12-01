import click
import resource

from . import ProjectConfigDecorator
    
from ..configs import (
    DatasetType,
    ProjectConfig
)
from ..dataset import IndexedDataset
from ..misc.IFactory import IFactory
from ..misc.IMeasurable import IMeasurable
from ..misc.ITrainable import ITrainable


@click.command()
@ProjectConfigDecorator
def train(project_config: ProjectConfig) -> None:
    """
    Encapsule l'entrainement
    """
    # TODO: a enlever
    # LIMITATION: Il est possible que python lance une erreur 'Too many file open'
    #             Je ne sais pas encore quel est la source du probleme mais un workaround
    #             est de hausser la limite avec 'ulimit -n 2048' ou utiliser le
    #             code python qui suit
    _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (project_config._ulimit_workaround, hard))

    train_config = project_config.train

    # validations
    if not isinstance(train_config.metrics, IMeasurable):
        raise ValueError(f"{type(train_config.metrics)} n'implemente pas IMeasurable")

    if not isinstance(train_config.trainer, ITrainable):
        raise ValueError(f"{type(train_config.trainer)} n'implemente pas ITrainable")

    if not isinstance(train_config.model_factory, IFactory):
        raise ValueError(f"{type(train_config.model_factory)} n'implemente pas IFactory")

    model = train_config.model_factory.create_from_config(project_config)

    train = IndexedDataset(project_config, DatasetType.TRAIN)
    validation = IndexedDataset(project_config, DatasetType.VALIDATION)

    train_config.trainer(project_config.paths,
                         train_config.parameters,
                         train_config.metrics,
                         model,
                         train.species_label,
                         train.spectrogram_groups, train.y,
                         validation.spectrogram_groups, validation.y)

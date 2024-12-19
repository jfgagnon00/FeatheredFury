import click
import platform

from ffury.cli import ProjectConfigDecorator
from ffury.configs import (
    DatasetType,
    ProjectConfig
)
from ffury.misc.logging import create_logger
from ffury.misc.Profile import Profile 
from ffury.misc.IFactory import IFactory
from ffury.misc.IMeasurable import IMeasurable
from ffury.misc.ITrainable import ITrainable

from ..dataset import IndexedDataset
from ..neptune.NeptuneRun import NeptuneRun


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

    if  platform.system() == "Darwin" :
        import resource
        _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (project_config._ulimit_workaround, hard))

    train_config = project_config.train

    # validations
    if not isinstance(train_config.measurable, IMeasurable):
        raise ValueError(f"{type(train_config.measurable)} n'implemente pas IMeasurable")

    if not isinstance(train_config.trainable, ITrainable):
        raise ValueError(f"{type(train_config.trainable)} n'implemente pas ITrainable")

    if not isinstance(train_config.model_factory, IFactory):
        raise ValueError(f"{type(train_config.model_factory)} n'implemente pas IFactory")

    with NeptuneRun(project_config) as run:
        with Profile() as profile:
            train = IndexedDataset.create(project_config, DatasetType.TRAIN)
            validation = IndexedDataset.create(project_config, DatasetType.VALIDATION)
            run.log_data_infos(train, validation)

            model = train_config.model_factory.create_from_config(project_config)

            train_config.trainable(run,
                                project_config.paths,
                                train_config.parameters,
                                train_config.measurable,
                                model,
                                train.species_label,
                                train.spectrogram_groups, train.y,
                                validation.spectrogram_groups, validation.y)
        
        run.log_duration(profile.duration)

        logger = create_logger(file=__file__)
        logger.info(f"Temps d'entrainement: {profile.round_duration()}s")

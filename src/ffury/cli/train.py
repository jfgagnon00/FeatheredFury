import click

from . import ConfigDecorator
from ..misc import Logger
from ..configs import MetaObject, load_config

from ..trainers import Generic  


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@ConfigDecorator
def train(config, filename):
    """
    Encapsule entrainement

    filename:
        Yaml contenant les parametres d'entrainement.
    """
    logger = Logger(True)

    parameters = load_config(filename)

    print(type(parameters.trainer))
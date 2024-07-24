import click

from . import ProjectConfigDecorator
from ..misc.logging import create_logger
from ..configs import load_config
# from ..trainers import Generic  


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@ProjectConfigDecorator
def train(config, filename):
    """
    Encapsule entrainement

    filename:
        Yaml contenant les parametres d'entrainement.
    """
    logger = create_logger(file=__file__)

    parameters = load_config(filename)

    logger.info(type(parameters.trainer))
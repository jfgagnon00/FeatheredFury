import click

from . import ProjectConfigDecorator
from ..configs import (
    ProjectConfig,
    TrainConfig
)

@click.command()
@ProjectConfigDecorator
def train(config):
    """
    Encapsule l'entrainement
    """
    print( config.train )

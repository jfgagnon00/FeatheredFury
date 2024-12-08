import click

from . import ProjectConfigDecorator
    
from ..configs import ProjectConfig
from ..misc.logging import create_logger


@click.command()
@ProjectConfigDecorator
def app(project_config: ProjectConfig) -> None:
    """
    Encapsule le demarrage de l'application
    """
    pass
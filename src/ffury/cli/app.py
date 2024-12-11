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
    from waitress import serve
    from ..application.app import create_app

    # Créer l'application Flask
    app = create_app()
    serve(app, host="0.0.0.0", port=5000)
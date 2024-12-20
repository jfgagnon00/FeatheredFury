import click

from . import ProjectConfigDecorator
    
from ..configs import ProjectConfig


@click.command()
@click.option("--secret", 
              type=str, 
              default="",
              help="Clef secrete")
@click.option("--debug", 
              is_flag=True, 
              default=False, 
              show_default=True, 
              help="Debug mode")
@ProjectConfigDecorator
def application(project_config: ProjectConfig,
                secret: str,
                debug: bool) -> None:
    """
    Encapsule le demarrage de l'application
    """
    from ..application import create_flask_app

    flask_app = create_flask_app(project_config, secret)
    flask_app.run(host=project_config.application.host,
                  port=project_config.application.port,
                  debug=debug)
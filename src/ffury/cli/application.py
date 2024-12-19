import click

from . import ProjectConfigDecorator
    
from ..configs import ProjectConfig


@click.command()
@click.option("--port", 
              type=int, 
              default=5000,
              help="Port de l'application")
@click.option("--host", 
              type=str, 
              default="0.0.0.0",
              help="Adresse pour host")
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
                port: int,
                host: str,
                secret: str,
                debug: bool) -> None:
    """
    Encapsule le demarrage de l'application
    """
    from ..application import create_flask_app

    flask_app = create_flask_app(project_config, secret)
    flask_app.run(host=host, 
                  port=port,
                  debug=debug)
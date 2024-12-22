import click

from typing import Union

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig


@click.command()
@click.option("--port", 
              type=int, 
              default=None,
              help="Override le port utilise")
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
                port: Union[int, None],
                secret: str,
                debug: bool) -> None:
    """
    Encapsule le demarrage de l'application
    """
    from .. import create_flask_app

    port = project_config.application.port if port is None else port

    flask_app = create_flask_app(project_config, secret)
    flask_app.run(host=project_config.application.host,
                  port=port,
                  debug=debug)
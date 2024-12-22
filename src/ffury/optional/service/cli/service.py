import click

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig
from ffury.misc.logging import create_logger
from typing import Union


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
def service(project_config: ProjectConfig,
            port: Union[int, None],
            secret: str,
            debug: bool) -> None:
    """
    Encapsule le demarrage du service
    """
    from .. import create_api

    port = project_config.service.port if port is None else port

    flask_service = create_api()
    flask_service.run(host=project_config.service.host,
                  port=port,
                  debug=debug)
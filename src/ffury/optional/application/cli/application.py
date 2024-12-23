import click

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig
from os import environ

from .. import create_flask_app


@click.command()
@click.option("--debug", 
              is_flag=True, 
              default=False, 
              show_default=True, 
              help="Debug mode")
@ProjectConfigDecorator
def application(project_config: ProjectConfig,
                debug: bool) -> None:
    """
    Encapsule le demarrage de l'application
    """
    if "FFURY_APPLICATION_PORT" in environ:
        port = environ["FFURY_APPLICATION_PORT"]
        if len(port) > 0:
            project_config.application.port = port

    if "FFURY_SERVICE_PORT" in environ:
        port = environ["FFURY_SERVICE_PORT"]
        if len(port) > 0:
            project_config.service.port = port

    if "FFURY_SERVICE_HOST" in environ:
        host = environ["FFURY_SERVICE_HOST"]
        if len(host) > 0:
            project_config.service.host = host

    flask_app = create_flask_app(project_config)
    flask_app.run(host=project_config.application.host,
                  port=project_config.application.port,
                  debug=debug)
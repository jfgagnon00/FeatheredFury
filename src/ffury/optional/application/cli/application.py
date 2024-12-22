import click

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig
from ffury.optional.azure.secrets import init_secrets
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
    init_secrets(["FFURY_APPLICATION_PORT", 
                  "FFURY_SERVICE_PORT",
                  "FFURY_SECRET"])

    if "FFURY_APPLICATION_PORT" in environ:
        project_config.application.port = environ["FFURY_APPLICATION_PORT"]

    if "FFURY_SERVICE_PORT" in environ:
        project_config.service.port = environ["FFURY_SERVICE_PORT"]

    if "FFURY_SECRET" in environ:
        project_config.service.secret = environ["FFURY_SECRET"]

    flask_app = create_flask_app(project_config)
    flask_app.run(host=project_config.application.host,
                  port=project_config.application.port,
                  debug=debug)
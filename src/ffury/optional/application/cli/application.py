import click

from ffury.misc.azure_secrets import init_secrets
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
    init_secrets("FFURY_APPLICATION_PORT", "FFURY_SECRET")

    port = project_config.application.port
    secret = ""

    if "FFURY_APPLICATION_PORT" in environ:
        port = environ["FFURY_APPLICATION_PORT"]

    if "FFURY_SECRET" in environ:
        secret = environ["FFURY_SECRET"]

    flask_app = create_flask_app(project_config, secret)
    flask_app.run(host=project_config.application.host,
                  port=port,
                  debug=debug)
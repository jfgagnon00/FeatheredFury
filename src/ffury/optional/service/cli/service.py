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
def service(project_config: ProjectConfig,
            debug: bool) -> None:
    """
    Encapsule le demarrage du service
    """
    init_secrets(["FFURY_SERVICE_PORT", "FFURY_SECRET"])

    if "FFURY_SERVICE_PORT" in environ:
        project_config.service.port = environ["FFURY_SERVICE_PORT"]

    if "FFURY_SECRET" in environ:
        project_config.service.secret = environ["FFURY_SECRET"]

    flask_service, swagger_service = create_flask_app(project_config)
    flask_service.run(host=project_config.service.host,
                      port=project_config.service.port,
                      debug=debug)
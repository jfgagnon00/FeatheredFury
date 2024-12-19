import click

from . import ProjectConfigDecorator
    
from ..configs import ProjectConfig
from ..misc.logging import create_logger


@click.command()
@ProjectConfigDecorator
def service(project_config: ProjectConfig) -> None:
    """
    Encapsule le demarrage du service
    """
    from waitress import serve
    from ..application import create_api 

    api = create_api()
 
    serve(api, host="0.0.0.0", port=8080)

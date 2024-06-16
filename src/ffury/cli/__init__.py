"""
Module encapsulant le commande line.
"""

import click

from .ProjectConfig import ProjectConfig
from .KaggleConfig import KaggleConfig
from ..configs import create_config, override_config, MetaObject

ConfigDecorator = click.make_pass_decorator(MetaObject)

@click.group()
@click.pass_context
@click.option("--config", 
              type=click.Path(exists=True), 
              default="ffury_configs.yaml",
              help="Configuration de projet")
def cli(ctx, config):
    # configurations par defaut
    project = ProjectConfig()
    dataset = KaggleConfig()

    # creation des overrides
    configOverrides = create_config(config)

    if not configOverrides is None:
        # appliquer overrides sur configiguration par defaut
        override_config(project, configOverrides.project)
        override_config(dataset, configOverrides.dataset)

    # encapsuler toutes les configs
    ctx.obj = MetaObject.from_kwargs(project=project,
                                     dataset=dataset)

def ffury():
    #
    # ajout de nouvelles commande line ici
    #
    from .dataset import dataset
    cli.add_command(dataset)

    # lance le command line
    cli()

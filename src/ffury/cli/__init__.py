"""
Module encapsulant le commande line.
"""

import click

from ..configs import (
    create_config, 
    MetaObject, 
    DEFAULT_CONFIG_FILE
)

ConfigDecorator = click.make_pass_decorator(MetaObject)

@click.group()
@click.pass_context
@click.option("--config", 
              type=click.Path(exists=True), 
              default=DEFAULT_CONFIG_FILE,
              help="Configuration de projet")
def _cli(ctx, config):
    # encapsuler toutes les configs
    ctx.obj = create_config(config)

def ffury():
    #
    # ajout de nouvelles commande line ici
    #
    from .dataset import dataset
    _cli.add_command(dataset)

    from .train import train
    _cli.add_command(train)

    # lance le command line
    _cli()

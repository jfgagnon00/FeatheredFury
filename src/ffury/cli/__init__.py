"""
Module encapsulant le commande line.
"""

import click

from ..configs import (
    load_config, 
    ProjectConfig,
    DEFAULT_CONFIG_FILE
)

ProjectConfigDecorator = click.make_pass_decorator(ProjectConfig)

@click.group()
@click.pass_context
@click.option("--config", 
              type=click.Path(exists=True), 
              default=DEFAULT_CONFIG_FILE,
              help="Configuration de projet")
def _cli(ctx, config):
    # toutes les commandes peuvent avoir acces
    # a la configuration de projet en utilisant 
    # ProjectConfigDecorator
    ctx.obj = load_config(config)

def ffury():
    # commandes doivent etre loadee afin d'etre utilisable
    # attention aux groupes de commndes; seulement le group
    # doit etre ajoute
    from .dataset import dataset_group
    from .dataset_install import install
    from .dataset_index import index
    from .dataset_preprocess import preprocess
    _cli.add_command(dataset_group)

    _cli()

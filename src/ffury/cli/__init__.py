"""
Module encapsulant le commande line.
"""

import click

from ..configs import (
    load_config, 
    ProjectConfig,
    DEFAULT_CONFIG_FILE
)

from ..misc.logging import create_logger


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

    logger = create_logger(file=__file__)

    # application et service
    from .application import app
    from .service import api
    _cli.add_command(application)
    _cli.add_command(service)

    try:
        logger.info("Module development installe.")

        from ..optional.development.cli.dataset import dataset_group
        from ..optional.development.cli.dataset_install import install
        from ..optional.development.cli.dataset_index import index
        from ..optional.development.cli.dataset_preprocess import preprocess
        _cli.add_command(dataset_group)

        from ..optional.development.cli.train import train
        _cli.add_command(train)
    except ImportError:
        logger.info("Module development non installe.")

    _cli()

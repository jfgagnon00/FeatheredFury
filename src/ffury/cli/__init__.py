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

    try:
        from ..optional.application.cli.application import application
        _cli.add_command(application)
    except ImportError:
        logger.info("Module application non installe.")

    try:
        from ..optional.service.cli.service import service
        _cli.add_command(service)
    except ImportError:
        logger.info("Module service non installe.")

    try:
        from ..optional.development.cli.dataset import dataset_group
        from ..optional.development.cli.dataset_install import install
        from ..optional.development.cli.dataset_index import index
        from ..optional.development.cli.dataset_preprocess import preprocess
        from ..optional.development.cli.dataset_reference import reference
        _cli.add_command(dataset_group)

        from ..optional.development.cli.train import train
        _cli.add_command(train)

        from ..optional.development.cli.neptune import neptune_group 
        from ..optional.development.cli.neptune_sync_model import sync_model
        _cli.add_command(neptune_group)
    except ImportError:
        logger.info("Module development non installe.")

    try:
        from ..optional.monitoring.cli.monitoring import monitoring_group
        from ..optional.monitoring.cli.monitoring_reference import (
            upload_reference, 
            download_reference
        )
        from ..optional.monitoring.cli.monitoring_drift_test import drift_test
        _cli.add_command(monitoring_group)
    except ImportError as e:
        logger.info("Module monitoring non installe.")

    _cli()

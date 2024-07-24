import click
import pathlib

from .dataset import dataset_group
from . import ProjectConfigDecorator
from ..misc.logging import create_logger
from tqdm import tqdm

@dataset_group.command()
# @click.argument("filename", type=click.Path(exists=True))
@ProjectConfigDecorator
def preprocess(config):
    """
    Preprocess du dataset (split + conversion HDF5)
    """
    logger = create_logger(file=__file__)
    logger.info("Done")

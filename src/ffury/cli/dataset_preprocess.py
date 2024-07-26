import click

from logging import Logger
from numpy.typing import ArrayLike
from pandas import (
    read_csv, 
    DataFrame
)
from sklearn.model_selection import train_test_split
from typing import(
    Tuple,
    Union
)

from . import ProjectConfigDecorator
from .dataset import dataset_group
from ..dataset._split import split
from ..dataset._preprocess import preprocess_parallel
from ..misc.logging import create_logger
from ..configs import (
    DatasetType,
    load_config,
    PreprocessConfig,
    ProjectConfig
)


@dataset_group.command()
@click.option("--config", 
              type=click.Path(exists=True), 
              default=None,
              help="Override preprocess config")
@ProjectConfigDecorator
def preprocess(project_config: ProjectConfig, 
               config: str) -> None:
    """
    Encapsule preprocess du dataset (split + conversion HDF5)
    """
    logger = create_logger(file=__file__)

    if not config is None:
        logger.info(f"Override preprocess config: '{config}'")
        project_config.preprocess = load_config(config)

    data_df = _load(logger, 
                    project_config.get_csv_filename(DatasetType.EXPLORED))
    
    train, test, validation = split(logger, 
                                    project_config.preprocess,
                                    data_df)
    
    _save(logger, 
          train, 
          project_config.get_csv_filename(DatasetType.TRAIN))
    _save(logger, 
          test, 
          project_config.get_csv_filename(DatasetType.TEST))
    _save(logger, 
          validation, 
          project_config.get_csv_filename(DatasetType.VALIDATION))

    preprocess_parallel(logger, 
                        project_config.preprocess, 
                        train,
                        test,
                        validation)

def _load(logger: Logger, 
          filename: str) -> DataFrame:
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"{data_df.shape[0]} elements")
    return data_df 

def _save(logger: Logger,
          data: DataFrame,
          filename: str) -> None:
    logger.info(f"Ecritudre de '{filename}'")
    data.to_csv(filename, index=False)

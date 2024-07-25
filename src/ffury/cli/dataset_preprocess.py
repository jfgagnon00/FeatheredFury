import click

from logging import Logger
from numpy.typing import ArrayLike
from pandas import read_csv, DataFrame
from sklearn.model_selection import train_test_split
from typing import(
    Tuple,
    Union
)

from .dataset import dataset_group
from . import ProjectConfigDecorator
from ..misc.logging import create_logger
from ..configs import (
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
                    project_config.get_dataset_explored_filename())
    train, test, validation = _split(logger, 
                                     data_df, 
                                     project_config)

def _load(logger: Logger, 
          filename: str) -> DataFrame:
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"{data_df.shape[0]} elements")
    return data_df 

def _split(logger: Logger, 
           data: DataFrame, 
           config: ProjectConfig) -> Tuple[DataFrame, DataFrame, DataFrame]:
    split_config = config.preprocess
    hold_ratio = split_config.split_train_size + split_config.split_test_size
    hold_size = int(data.shape[0] * hold_ratio)

    validation_size = data.shape[0] - hold_size
    test_size = int(data.shape[0] * split_config.split_test_size)
    train_size = data.shape[0] - test_size - validation_size

    logger.info(f"Train size     : {train_size}")
    logger.info(f"Test size      : {test_size}")
    logger.info(f"Validation size: {validation_size}")

    # validation size sont valides
    assert_size = train_size + test_size + validation_size
    if train_size <= 0 or \
       test_size <= 0 or \
       validation_size <= 0 or \
       assert_size != data.shape[0]:
        raise ValueError("train_size et/ou test_size ne semblent pas valide")
    
    train, validation = train_test_split(data, 
                                         train_size=hold_size, 
                                         stratify=_get_stratify(split_config, data),)
    
    train, test = train_test_split(train, 
                                   train_size=train_size, 
                                   stratify=_get_stratify(split_config, train))
    
    # validation split donne resultat attendu
    assert train.shape[0] == train_size
    assert test.shape[0] == test_size
    assert validation.shape[0] == validation_size

    # sauvegarder les splits
    _write_csv(logger, train, config.get_dataset_train_filename())
    _write_csv(logger, test, config.get_dataset_test_filename())
    _write_csv(logger, validation, config.get_dataset_validation_filename())

    return train, test, validation

def _get_stratify(config: PreprocessConfig, 
                  data: DataFrame) -> Union[ArrayLike, None]:
    if config.split_stratify_on is None:
        return None

    return data[config.split_stratify_on]

def _write_csv(logger: Logger,
               data: DataFrame,
               filename: str) -> None:
    logger.info(f"Ecritudre de '{filename}'")
    data.to_csv(filename, index=False)

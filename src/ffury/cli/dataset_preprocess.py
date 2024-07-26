import click

from logging import Logger
from pandas import (
    read_csv, 
    DataFrame
)
from sklearn.model_selection import train_test_split

from . import ProjectConfigDecorator
from .dataset import dataset_group
from ..configs import (
    DatasetType,
    load_config,
    ProjectConfig
)
from ..dataset._BirdCLEF._ParallelPreprocessor import ParallelPreprocessor
from ..dataset._hdf5 import create_file
from ..dataset._split import split
from ..misc.concurrent import create_thread_pool_executor
from ..misc.logging import create_logger


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
    
    with create_thread_pool_executor() as executor:
        preprocessor = ParallelPreprocessor(logger,
                                            project_config.preprocess,
                                            executor)
        for data, type_ in [(train, DatasetType.TRAIN),
                            (test, DatasetType.TEST),
                            (validation, DatasetType.VALIDATION)]:
            _save(logger, 
                  data, 
                  project_config.get_csv_filename(type_))

            logger.info(f"Preprocessing {type_.name_lowercase}")
            filename = project_config.get_hdf5_filename(type_)
            with create_file(filename, "w") as f:
                preprocessor.run(f, data)

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

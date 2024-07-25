from logging import Logger
from pandas import DataFrame

from ..configs import PreprocessConfig

def _preprocess_parallel_dataframe(logger: Logger,
                                config: PreprocessConfig, 
                                data: DataFrame) -> None:
    pass

def preprocess_parallel(logger: Logger,
                        config: PreprocessConfig, 
                        train: DataFrame,
                        test: DataFrame,
                        validation: DataFrame) -> None:
    for data, name in [ (train, "train"), 
                        (test, "test"),
                        (validation, "validation") ]:
        logger.info(f"Processing {name}")
        _preprocess_parallel_dataframe(logger, config, data)

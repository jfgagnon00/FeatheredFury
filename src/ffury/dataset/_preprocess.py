from logging import Logger
from pandas import DataFrame
from tqdm import tqdm

from ..configs import PreprocessConfig
from ..misc.concurrent import (
    create_thread_pool_executor,
    parallel_for
)


def _preprocess_parallel_dataframe(logger: Logger,
                                   config: PreprocessConfig, 
                                   data: DataFrame) -> None:
    # une autre table qui a nom commun et one hot encode
    # mon data est spectrogram, lat, long, espece (one hot encode)
    pass

def preprocess_parallel(logger: Logger,
                        config: PreprocessConfig, 
                        train: DataFrame,
                        test: DataFrame,
                        validation: DataFrame) -> None:
    with create_thread_pool_executor() as executor:
        for data, name in [ (train, "train"), 
                            (test, "test"),
                            (validation, "validation") ]:
            logger.info(f"Processing {name}")
            _preprocess_parallel_dataframe(logger, config, data)

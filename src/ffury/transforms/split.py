from pandas import DataFrame
from sklearn.model_selection import train_test_split
from typing import Tuple

from .properties import _SPECIE

from ..configs import PreprocessConfig
from ..misc.logging import create_logger


def split(data: DataFrame,
          config: PreprocessConfig) -> Tuple[DataFrame, DataFrame, DataFrame]:
    hold_ratio = config.split_train_size + config.split_test_size
    hold_size = int(data.shape[0] * hold_ratio)

    validation_size = data.shape[0] - hold_size
    test_size = int(data.shape[0] * config.split_test_size)
    train_size = data.shape[0] - test_size - validation_size

    logger = create_logger(file=__file__)
    logger.info(f"Train size     : {train_size}")
    logger.info(f"Test size      : {test_size}")
    logger.info(f"Validation size: {validation_size}")

    # validation size
    assert_size = train_size + test_size + validation_size
    if train_size <= 0 or \
       test_size <= 0 or \
       validation_size <= 0 or \
       assert_size != data.shape[0]:
        raise ValueError("train_size et/ou test_size ne semblent pas valide")
    
    train, validation = train_test_split(data, 
                                         train_size=hold_size, 
                                         stratify=data[_SPECIE])
    
    train, test = train_test_split(train, 
                                   train_size=train_size, 
                                   stratify=train[_SPECIE])
    
    # validation split donne resultat attendu
    assert train.shape[0] == train_size
    assert test.shape[0] == test_size
    assert validation.shape[0] == validation_size

    return train, test, validation

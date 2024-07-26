from concurrent.futures import (
    Executor,
    wait
)
from h5py import File
from logging import Logger, DEBUG
from numpy import (
    eye,
    uint8,
    int32 as np_int32
)
from numpy.typing import NDArray
from pandas import (
    Categorical,
    DataFrame
)
from tqdm import tqdm

from .._hdf5 import (
    join_keys,
    _STRING_ENCODING,
    _STRING_DTYPE
)
from ...configs import PreprocessConfig
from ...misc.concurrent import parallel_for

SPECIES_KEY = "species"

PRIMARY_LABEL = "primary_label"
COMMON_NAME = "common_name"
ONE_HOT_ENCODING = "one_hot_encoding"

class ParallelPreprocessor:
    def __init__(self, 
                 logger: Logger,
                 config: PreprocessConfig, 
                 executor: Executor) -> None:
        self._logger = logger
        self._config = config
        self._executor = executor

    def run(self, 
            h5_file: File,
            data: DataFrame) -> None:
        count = data.shape[0]

        with tqdm(total=count) as progress:
            species_future = self._executor.submit(self._preprocess_species, 
                                                   h5_file,
                                                   data)

            wait([species_future])

    def _preprocess_species(self,
                            h5_file: File,
                            data: DataFrame) -> NDArray[np_int32]:
        # regrouper primary_label et common_name a partir du dataframe
        # les 2 proprietes sont uniques; represente espece
        lookup = data[[PRIMARY_LABEL, COMMON_NAME]].groupby(PRIMARY_LABEL).first()
        lookup.reset_index(inplace=True)

        # fixer encodage hdf5
        primary_labels = []
        common_names = []
        for _, row in lookup.iterrows():
            primary_labels.append( row[PRIMARY_LABEL].encode(_STRING_ENCODING) )
            common_names.append( row[COMMON_NAME].encode(_STRING_ENCODING) )

        h5_file.create_dataset(join_keys(SPECIES_KEY, PRIMARY_LABEL),
                               data=primary_labels,
                               dtype=_STRING_DTYPE)
        
        h5_file.create_dataset(join_keys(SPECIES_KEY, COMMON_NAME),
                               data=common_names,
                               dtype=_STRING_DTYPE)
        
        h5_file.create_dataset(join_keys(SPECIES_KEY, ONE_HOT_ENCODING),
                               data=eye(lookup.shape[0], dtype=uint8),
                               dtype=uint8)

        # transformer information d'espece en index (plus compacte sur disque)
        indices = Categorical(data[PRIMARY_LABEL], 
                              categories=lookup[PRIMARY_LABEL],
                              dtype=np_int32)

        # validation
        assert lookup.shape[0] == indices.codes.shape[0]

        return indices

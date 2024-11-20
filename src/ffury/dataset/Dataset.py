from pandas import (
    DataFrame,
    read_csv
)

from .hdf5 import open_file
from .preprocess import (
    _MELSPECTROGRAM_GROUPS,
    _SPECIE,
    _LATITUDE,
    _LONGITUDE
)
from ..configs import (
    DatasetType,
    ProjectConfig
)


class Dataset():
    """
    Encapsuler le format et l'organisation des donnees. Utilisateur ne voit que des objets
    de style nympy array
    """
    def __init__(self, project_config: ProjectConfig, dataset_type: DatasetType):
        self._init_species_label(project_config)
        self._init_dataset(project_config, dataset_type)

    @property
    def species_label(self):
        return self._species_label

    @property
    def species_label(self):
        return self._species_label
    
    @property
    def dataframe(self):
        return self._dataframe

    @property
    def melspectrogram_groups(self):
        return self._melspectrogram_groups

    def _init_species_label(self, project_config: ProjectConfig):
        filename = project_config.get_csv_filename(DatasetType._SPECIES)
        species_df = read_csv(filename)
        self._species_label = species_df["common_name"].to_list()

    def _init_dataset(self, project_config: ProjectConfig, dataset_type: DatasetType):
        filename = project_config.get_hdf5_filename(dataset_type)
        self._hdf5_file = open_file(filename, "r")
        self._dataframe = DataFrame({
                _SPECIE: self._hdf5_file[_SPECIE],
                _LATITUDE: self._hdf5_file[_LATITUDE],
                _LONGITUDE: self._hdf5_file[_LONGITUDE]
            }
        )
        self._melspectrogram_groups = self._hdf5_file[_MELSPECTROGRAM_GROUPS]

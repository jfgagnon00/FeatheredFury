from pandas import (
    DataFrame,
    read_csv
)

from .hdf5 import open_file
from ..configs import (
    DatasetType,
    ProjectConfig
)
from ..transforms.properties import (
    _LATITUDE,
    _LONGITUDE,
    _SPECIE,
    _SPECTROGRAM_GROUPS
)


class IndexedDataset():
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
    def y(self):
        return self._y

    @property
    def lat_long(self):
        return self._lat_long

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
        self._y = DataFrame({
                _SPECIE: self._hdf5_file[_SPECIE],
            })
        self._lat_long = DataFrame({
                _LATITUDE: self._hdf5_file[_LATITUDE],
                _LONGITUDE: self._hdf5_file[_LONGITUDE]
            })
        self._melspectrogram_groups = self._hdf5_file[_SPECTROGRAM_GROUPS]

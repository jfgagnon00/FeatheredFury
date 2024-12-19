from pandas import (
    DataFrame,
    read_csv
)

from ffury.configs import (
    DatasetType,
    ProjectConfig
)

from ..misc.hdf5 import open_file
from ..transforms import (
    read_indexing_md5,
    read_split_sampling_md5
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
    de style nympy array ou pandas DataFRame
    """
    @staticmethod
    def create(project_config: ProjectConfig, dataset_type: DatasetType):
        """
        Methode recommende pour la creation de IndexedDataset. Effectue quelques verifications
        afin de s'assurer de la consistence des donnees
        """
        # valider split/sample md5 est consistent avec la config demande
        md5_preprocessed = read_split_sampling_md5(project_config)
        if md5_preprocessed != project_config.preprocess.split_sampling_md5():
            # ces changements demande une nouvelle version des donnees
            raise ValueError("Parmetres de split/sampling ne semblent pas compatible avec configuration. " 
                             "Lancer le preprocess de nouveau")

        # valider spectrogram md5 est consistent avec la config demande
        md5_indexed = read_indexing_md5(project_config)
        if md5_indexed != project_config.preprocess.spectrogram_md5():
            # TODO: lancer indexation automatique
            raise ValueError("Parmetres de spectrogramme ne semblent pas compatible avec configuration. " 
                             "Lancer l'indexation de nouveau")

        # creation dataset indexe
        return IndexedDataset(project_config, 
                              dataset_type, 
                              md5_preprocessed,
                              md5_indexed)

    def __init__(self, project_config: ProjectConfig, 
                 dataset_type: DatasetType,
                 md5_preprocessed: str,
                 md5_indexed: str) -> None:
        self._md5_preprocessed = md5_preprocessed
        self._md5_indexed = md5_indexed
        self._init_species_label(project_config)
        self._init_dataset(project_config, dataset_type)

    @property
    def md5_preprocessed(self):
        return self._md5_preprocessed

    @property
    def md5_indexed(self):
        return self._md5_indexed

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
    def spectrogram_groups(self):
        return self._spectrogram_groups

    def _init_species_label(self, project_config: ProjectConfig):
        filename = project_config.get_csv_filename(DatasetType._SPECIES)
        species_df = read_csv(filename)
        self._species_label = species_df["common_name"].to_list()

    def _init_dataset(self, project_config: ProjectConfig, dataset_type: DatasetType):
        filename = project_config.get_hdf5_filename(dataset_type)
        self._hdf5_file = open_file(filename, "r")
        self._y = self._hdf5_file[_SPECIE]
        self._lat_long = DataFrame({
                _LATITUDE: self._hdf5_file[_LATITUDE],
                _LONGITUDE: self._hdf5_file[_LONGITUDE]
            })
        self._spectrogram_groups = self._hdf5_file[_SPECTROGRAM_GROUPS]

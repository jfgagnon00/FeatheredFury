from h5py import (
    VirtualLayout, 
    VirtualSource
)
from numpy import (
    int32,
    float32
)
from numpy.typing import NDArray
from pandas import (
    Categorical,
    DataFrame,
    Index
)
from pandas import read_csv
from pandas.api.typing import DataFrameGroupBy
from pathlib import Path
from sklearn.model_selection import train_test_split
from typing import Tuple

from ..configs import PreprocessConfig
from ..dataset.hdf5 import open_file
from ..misc.halton import halton_sequence

_MELSPECTROGRAM_GROUPS = "melspectrogram_groups"
_MELSPECTROGRAM = "melspectrogram"
_SPECIE = "specie"
_SPECIES_CSV = "data_species.csv"
_PRIMARY_LABEL = "primary_label"
_COMMON_NAME = "common_name"
_FILENAME = "filename"
_LATITUDE = "latitude"
_LONGITUDE = "longitude"
_DURATION = "Duration"


def generate_species_groups(data: DataFrame) -> tuple[DataFrameGroupBy, DataFrame, Index]:
    """
    Extrait les informations d'especes

    Parametres:
        data: Le dataset explore.

    Retour:
        Tuple (data regroupe par espece, dataset avec primary_label et common_name, index des especes)

    Note:
        L'index des especes permet de trouver un nom a partir d'un entier et de retrouver 
        l'entier a partir d'un nom. Facilite les traitements subsequents.
    """
    # regrouper les attributs par espece
    species_groups = data.groupby(_PRIMARY_LABEL)
    
    # regrouper primary_label et common_name a partir du dataframe
    # les 2 proprietes sont uniques; represente espece
    species_str = data[[_PRIMARY_LABEL, _COMMON_NAME]].groupby(_PRIMARY_LABEL).first()
    species_str.reset_index(inplace=True)

    # transformer information d'espece en index (plus compacte sur disque)
    # one hot encoding pourra etre facilement reconstruit a partir de cet index
    species_categories = Categorical(data[_PRIMARY_LABEL],
                                     categories=species_str[_PRIMARY_LABEL])

    # validation
    assert data.shape[0] == species_categories.shape[0]

    return species_groups, species_str, species_categories.categories

def generate_specie_groups(dataframe_filename: str,
                           dataframe_mode: str,
                           hdf5_spectrogram_path: str,
                           specie_infos: DataFrame,
                           specie_str: str,
                           specie_code: int,
                           config: PreprocessConfig) -> None:
    """
    Resample l'audio d'une espece complete pour avoir une quantite fixe de groupes
    """
    # validation
    if config.group_count < 1:
        raise ValueError(f"group_count < 1: {config.group_count}")

    # construire structure pour remapper nombre [0, 1] a index dans specie_infos
    # doit tenir compte de spectrogram_length
    length = 0
    lengths = []
    for index, duration in specie_infos[_DURATION].items():
        spectrogram_frame_length = duration * 1000 / config.spectrogram_stft_frame_size_ms
        spectrogram_frame_length = int(spectrogram_frame_length) + 1

        lengths.append((index, spectrogram_frame_length, length, length + spectrogram_frame_length))
        length += spectrogram_frame_length

    # determiner la quantite de frames necessaire pour (group, segment, group_hop)
    group_frame_length, \
        segment_frame_length, \
        group_hop_frame_length = config.group_info()

    group_datas = {
        "hdf5_source": [],
        "dataset": [],
        "spectrogram_frame_length": [],
        "group_begin": [],
        "segment_frame_length": [],
        "group_hop_frame_length": [],
        _LATITUDE: [],
        _LONGITUDE: [],
        _SPECIE: [],
    }

    # generer les groupes
    for g, t in enumerate(halton_sequence(3, config.group_count)):
        # ramapper [0, 1] a [0, length]
        group_begin = int(t * length)

        # trouver le fichier et la position dans le fichier qui 
        # correspond a group_begin
        for index, spectrogram_frame_length, begin, end in lengths:
            if end > group_begin:
                break
        group_begin = group_begin - begin
        group_end = group_begin + group_frame_length

        # clamper avec les limites du fichier
        if group_end > spectrogram_frame_length:
            group_end = spectrogram_frame_length
            group_begin = spectrogram_frame_length - group_frame_length

        # sauvegarder information
        hdf5_source = Path.joinpath(hdf5_spectrogram_path, 
                                    specie_infos.loc[index, _FILENAME])
        hdf5_source = hdf5_source.with_suffix(".hdf5")

        group_datas["hdf5_source"].append(hdf5_source)
        group_datas["dataset"].append(_MELSPECTROGRAM)
        group_datas["spectrogram_frame_length"].append(spectrogram_frame_length)
        group_datas["group_begin"].append(group_begin)
        group_datas["segment_frame_length"].append(segment_frame_length)
        group_datas["group_hop_frame_length"].append(group_hop_frame_length)
        group_datas[_LATITUDE].append( specie_infos.loc[index, _LATITUDE] )
        group_datas[_LONGITUDE].append( specie_infos.loc[index, _LONGITUDE] )
        group_datas[_SPECIE].append( specie_code )

    dataframe_filename = Path(dataframe_filename)
    dataframe_filename.parent.mkdir(exist_ok=True, parents=True)

    DataFrame(group_datas).to_csv(dataframe_filename, mode=dataframe_mode, index=False, header=dataframe_mode=="w")

def write_hdf5_dataset(hdf5_filename: str,
                       hdf5_mode: str,
                       dataset: str,
                       data: NDArray) -> None:
    filename = Path(hdf5_filename)
    filename.parent.mkdir(exist_ok=True, parents=True)

    with open_file(filename, hdf5_mode) as hdf5_file:
        hdf5_file.create_dataset(dataset, data=data)
        hdf5_file.flush()

def write_species_dataframe(filename: str,
                            species_str: DataFrame) -> None:
    filename = Path(filename)
    filename.parent.mkdir(exist_ok=True, parents=True)
    species_str.to_csv(filename, index=False)

def split(dataframe_filename: str,
          config: PreprocessConfig) -> Tuple[DataFrame, DataFrame, DataFrame]:
    df = read_csv(dataframe_filename)

    train, other = train_test_split(df, 
                                    train_size=config.split_train_size,
                                    stratify=df[_SPECIE])
    test, validation = train_test_split(other,
                                        train_size=config.split_test_size,
                                        stratify=other[_SPECIE])

    return train, test, validation

def write_hdf5_groups(hdf5_filename: str,
                      hdf5_mode: str,
                      data_df: DataFrame,
                      config: PreprocessConfig) -> None:
    hdf5_filename = Path(hdf5_filename)
    hdf5_filename.parent.mkdir(exist_ok=True, parents=True)
    with open_file(hdf5_filename, hdf5_mode) as hdf5_file:
        hdf5_file.create_dataset(_LATITUDE,
                                 data=data_df[_LATITUDE].astype(float32))
        
        hdf5_file.create_dataset(_LONGITUDE,
                                 data=data_df[_LONGITUDE].astype(float32))
        
        hdf5_file.create_dataset(_SPECIE,
                                 data=data_df[_SPECIE].astype(int32))

        # les groupes sont des vues sur d'autres fichiers hdf5
        # d'ou VirtualLayout et create_virtual_dataset
        group_shape = (data_df.shape[0],
                       config.group_segment_count, 
                       config.spectrogram_n_mels,
                       data_df.iloc[0].segment_frame_length)
        group_layout = VirtualLayout(# batch, n_segments, n_mels, n_frames)
                                     shape=group_shape,
                                     dtype=float32)
        
        for g in range(0, data_df.shape[0], config.group_segment_count):
            r = data_df.iloc[g]
            source = VirtualSource(r.hdf5_source, 
                                   r.dataset,
                                   (config.spectrogram_n_mels, r.spectrogram_frame_length),
                                   dtype=float32)
            
            segment_begin = r.group_begin
            for s in range(config.group_segment_count):
                segment_end = segment_begin + r.segment_frame_length
                group_layout[g, s, ...] = source[..., segment_begin:segment_end]
                segment_begin = r.group_hop_frame_length

        hdf5_file.create_virtual_dataset(_MELSPECTROGRAM_GROUPS, group_layout)
        hdf5_file.flush()

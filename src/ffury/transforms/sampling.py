from pandas import (
    Categorical,
    DataFrame,
    Index
)
from pandas.api.typing import DataFrameGroupBy
from pathlib import Path
from shutil import copyfile

from .properties import (
    _AUDIO,
    _COMMON_NAME,
    _DURATION_MS,
    _FILENAME,
    _GROUP_BEGIN,
    _GROUP_HOP_FRAME_LENGTH,
    _LATITUDE,
    _LONGITUDE,
    _PRIMARY_LABEL,
    _SEGMENT_FRAME_LENGTH,
    _SPECIE,
    _SPECTROGRAM_FRAME_LENGTH,
)

from ..configs import (
    ProjectConfig,
    PreprocessConfig
)
from ..misc.halton import halton_sequence


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

def generate_specie_groups(specie_infos: DataFrame,
                           specie_code: int,
                           config: PreprocessConfig) -> DataFrame:
    """
    Resample specie_infos pour avoir une quantite fixe de groupes
    """
    # validation
    if config.group_count < 1:
        raise ValueError(f"group_count < 1: {config.group_count}")

    # construire structure pour remapper nombre [0, 1] a index dans specie_infos
    # doit tenir compte de spectrogram_length
    length = 0
    lengths = []
    for index, duration_ms in specie_infos[_DURATION_MS].items():
        # estimer de la longeur en framew du spectrograme a partir 
        # de la duree du fichier audio et la fenetre de transformation du spectrogramme
        spectrogram_frame_length = duration_ms / config.spectrogram_stft_frame_size_ms
        spectrogram_frame_length = int(spectrogram_frame_length) + 1

        # index dans specie_infos, taille spectrogramme, quand debute le fichier courant, quand termine le fichier courant
        lengths.append((index, spectrogram_frame_length, length, length + spectrogram_frame_length))
        length += spectrogram_frame_length

    # determiner la quantite de frames necessaire pour (group, segment, group_hop)
    group_frame_length, \
        segment_frame_length, \
        group_hop_frame_length = config.group_info()

    # donnees a sauvegarder par groupe
    group_datas = {
        _FILENAME: [],
        _SPECTROGRAM_FRAME_LENGTH: [],
        _GROUP_BEGIN: [],
        _SEGMENT_FRAME_LENGTH: [],
        _GROUP_HOP_FRAME_LENGTH: [],
        _LATITUDE: [],
        _LONGITUDE: [],
        _SPECIE: [],
    }

    # generer les groupes
    for t in halton_sequence(3, config.group_count):
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
        group_datas[_FILENAME].append(specie_infos.loc[index, _FILENAME])
        group_datas[_SPECTROGRAM_FRAME_LENGTH].append(spectrogram_frame_length)
        group_datas[_GROUP_BEGIN].append(group_begin)
        group_datas[_SEGMENT_FRAME_LENGTH].append(segment_frame_length)
        group_datas[_GROUP_HOP_FRAME_LENGTH].append(group_hop_frame_length)
        group_datas[_LATITUDE].append( specie_infos.loc[index, _LATITUDE] )
        group_datas[_LONGITUDE].append( specie_infos.loc[index, _LONGITUDE] )
        group_datas[_SPECIE].append( specie_code )

    return DataFrame(group_datas)

def copy_specie_groups_data(specie_data: DataFrame,
                            config: ProjectConfig) -> None:
    """
    Fait une copie des fichiers trouves dans specie_data pour fin
    de versionning.
    """
    for f in specie_data[_FILENAME].unique():
        src = config.get_audio_filename(f)
        dst = Path.joinpath(config.paths.DATA_DIR, _AUDIO, f)
        dst.parent.mkdir(exist_ok=True, parents=True)
        copyfile(src, dst)

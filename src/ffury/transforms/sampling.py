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
    _GROUP_BEGIN_MS,
    _LATITUDE,
    _LONGITUDE,
    _PRIMARY_LABEL,
    _SPECIE
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
    total_duration_ms = 0
    duration_ms_infos = []
    for index, duration_ms in specie_infos[_DURATION_MS].items():
        # index, duration, begin, end
        duration_ms_infos.append((index, duration_ms, total_duration_ms, total_duration_ms + duration_ms))
        total_duration_ms += duration_ms

    # determiner la quantite de frames necessaire pour (group, segment, group_hop)
    group_ms_length, _, _ = config.group_ms_infos()

    # donnees a sauvegarder par groupe
    group_datas = {
        _FILENAME: [],
        _SPECIE: [],
        _LATITUDE: [],
        _LONGITUDE: [],
        _DURATION_MS: [],
        _GROUP_BEGIN_MS: [],
    }

    # generer les groupes
    for t in halton_sequence(3, config.group_count):
        # ramapper [0, 1] a [0, total_duration_ms]
        group_begin_ms = int(t * total_duration_ms)

        # trouver le fichier et la position dans le fichier qui 
        # correspond a group_begin
        for index, duration_ms, begin_ms, end_ms in duration_ms_infos:
            if end_ms > group_begin_ms:
                break

        group_begin_ms = group_begin_ms - begin_ms
        group_end_ms = group_begin_ms + group_ms_length

        # clamper avec les limites du fichier
        if group_end_ms > duration_ms:
            group_begin_ms = duration_ms - group_ms_length

        # sauvegarder information
        group_datas[_FILENAME].append(specie_infos.loc[index, _FILENAME])
        group_datas[_LATITUDE].append( specie_infos.loc[index, _LATITUDE] )
        group_datas[_LONGITUDE].append( specie_infos.loc[index, _LONGITUDE] )
        group_datas[_SPECIE].append( specie_code )
        group_datas[_DURATION_MS].append(duration_ms)
        group_datas[_GROUP_BEGIN_MS].append(group_begin_ms)

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

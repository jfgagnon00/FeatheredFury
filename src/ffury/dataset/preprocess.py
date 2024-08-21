from librosa import (
    power_to_db,
    resample,
    to_mono
)
from librosa.feature import melspectrogram
from pandas import (
    Categorical,
    DataFrame,
    Index
)
from pandas.api.typing import DataFrameGroupBy
from numpy import (
    max as np_max,
)
from numpy.typing import NDArray
from typing import Generator
from ..configs import PreprocessConfig


_MELSPECTROGRAM_SEGMENT = "melspectrogram_segments"
_MELSPECTROGRAM = "melspectrogram"
_SPECIE = "specie"
_SPECIES_CSV = "data_species.csv"
_PRIMARY_LABEL = "primary_label"
_COMMON_NAME = "common_name"
_FILENAME = "filename"
_LATITUDE = "latitude"
_LONGITUDE = "longitude"


def generate_spectrogram(audio: NDArray,
                         sampling_rate: int,
                         config: PreprocessConfig) -> NDArray:
    """
    # Separe audio en plusieurs segments (selon config) et genere leurs spectrograms
    """
    if audio.shape[0] > 1:
        audio = to_mono(audio)

    if sampling_rate != config.clip_sampling_rate_hz:
        audio = resample(audio,
                         orig_sr=sampling_rate,
                         target_sr=config.clip_sampling_rate_hz)

    # log mel spectrogram
    S = melspectrogram(y=audio,
                       sr=config.clip_sampling_rate_hz,
                       n_fft=config.spectrogram_n_ftt,
                       hop_length=config.spectrogram_hop_length,
                       n_mels=config.spectrogram_n_mels,
                       fmin=config.spectrogram_fmin,
                       fmax=config.spectrogram_fmax)

    S_db = power_to_db(S,
                       ref=np_max)

    # shape du spectrogram est (n_mels, time)
    # si on veut ajouter plus tard, c'est plus simple d'avoir (time, n_mels)
    return S_db.T

def get_num_segments(spectrogram_length: int,
                     config: PreprocessConfig) -> int:
    return spectrogram_length // config.spectrogram_segment_hop_length

def generate_segments(spectrogram_length: int,
                      config: PreprocessConfig) -> Generator[int, None, None]:
    length = config.spectrogram_segment_length
    hop = config.spectrogram_segment_hop_length

    for offset in range(0, spectrogram_length, hop):
        start = offset
        end = offset + length

        if end >= spectrogram_length:
            # imcomplete segment
            break

        yield start, end

def generate_species_groups(data: DataFrame) -> tuple[DataFrameGroupBy, DataFrame, Index]:
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
from librosa import (
    power_to_db,
    resample,
    to_mono
)
from librosa.feature import melspectrogram
from pandas import (
    Categorical,
    DataFrame
)
from numpy import (
    max as np_max,
    pad,
)
from numpy.typing import NDArray
from typing import List
from ..configs import PreprocessConfig


_MELSPECTROGRAM = "melspectrogram"
_SPECIE = "specie"
_SPECIES_CSV = "data_species.csv"
_PRIMARY_LABEL = "primary_label"
_COMMON_NAME = "common_name"
_FILENAME = "filename"
_LATITUDE = "latitude"
_LONGITUDE = "longitude"


def generate_segment_spectrograms(audio: NDArray,
                                  sampling_rate: int,
                                  config: PreprocessConfig) -> List[NDArray]:
    """
    Separe audio en plusieurs segments (selon config) et genere leurs spectrograms
    """
    if len(audio) > 1:
        audio = to_mono(audio)

    if sampling_rate != config.clip_sampling_rate_hz:
        audio = resample(audio,
                            orig_sr=sampling_rate,
                            target_sr=config.clip_sampling_rate_hz)
        
    segment_length = config.segment_length
    segment_hop = config.segment_hop_length

    spectrograms = []

    for offset in range(0, len(audio), segment_hop):
        # extraire segment
        segment = audio[offset:offset + segment_length]

        # padding sur le dernier segment
        padding = segment_length - len(segment)
        if padding > 0:
            segment = pad(segment, (0, padding), mode="wrap")

        # log mel spectrogram
        S = melspectrogram(y=segment,
                            sr=config.clip_sampling_rate_hz,
                            n_fft=config.spectrogram_n_ftt,
                            hop_length=config.spectrogram_hop_length,
                            n_mels=config.spectrogram_n_mels,
                            fmin=config.spectrogram_fmin,
                            fmax=config.spectrogram_fmax)

        S_db = power_to_db(S,
                           ref=np_max)

        # ajouter aux resultats
        spectrograms.append(S_db)

    return spectrograms

def generate_uinique_species(data: DataFrame) -> tuple[DataFrame, NDArray]:
    # regrouper primary_label et common_name a partir du dataframe
    # les 2 proprietes sont uniques; represente espece
    species_str = data[[_PRIMARY_LABEL, _COMMON_NAME]].groupby(_PRIMARY_LABEL).first()
    species_str.reset_index(inplace=True)

    # transformer information d'espece en index (plus compacte sur disque)
    # one hot encoding pourra etre facilement reconstruit a partir de cet index
    species_codes = Categorical(data[_PRIMARY_LABEL],
                                categories=species_str[_PRIMARY_LABEL])

    # validation
    assert data.shape[0] == species_codes.shape[0]

    return species_str, species_codes.codes
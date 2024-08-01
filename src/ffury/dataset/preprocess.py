from librosa import (
    power_to_db,
    resample,
    to_mono
)
from librosa.feature import melspectrogram
from numpy import (
    max as np_max,
    pad,
)
from numpy.typing import NDArray
from typing import List
from ..configs import PreprocessConfig

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

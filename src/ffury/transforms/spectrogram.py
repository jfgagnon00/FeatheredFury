import numpy as np

from librosa import power_to_db
from librosa.feature import melspectrogram
from librosa.util import normalize
# from numpy import (
#     max as np_max,
#     min as np_min,
#     mean as np_mean,
#     std as np_std,
#     abs as np_abs
#     where
# )
from numpy.typing import NDArray
from sklearn.preprocessing import (
    MinMaxScaler,
    StandardScaler
)

from ..configs import PreprocessConfig
from .waveform import waveform_apply_config

def spectrogram_from_audio(audio: NDArray,
                           sampling_rate: int,
                           config: PreprocessConfig) -> NDArray:
    """
    # Genere melspectrogram de audio
    """
    if config.spectrogram_stft_window_size_ms < config.spectrogram_stft_frame_size_ms:
        raise ValueError(f"spectrogram_stft_window_size_ms {config.spectrogram_stft_window_size_ms} < spectrogram_stft_frame_size_ms {config.spectrogram_stft_frame_size_ms}")

    if sampling_rate != config.clip_sampling_rate_hz:
        raise ValueError(f"sampling_rate {sampling_rate} != clip_sampling_rate_hz {config.clip_sampling_rate_hz}")

    if len(audio.shape) > 1 and audio.shape[1] != 1:
        raise ValueError(f"audio.shape {audio.shape} is not mono")

    S = melspectrogram(y=audio,
                       power=config.spectrogram_power,
                       sr=config.clip_sampling_rate_hz,
                       n_fft=config.spectrogram_n_ftt,
                       hop_length=config.spectrogram_hop_length,
                       n_mels=config.spectrogram_n_mels,
                       fmin=config.spectrogram_fmin,
                       fmax=config.spectrogram_fmax)

    S_db = power_to_db(S, ref=np.max)

    # normalisation
    S_db = normalize(S_db)

    if False:
        # masking
        Z_SCALE = 0.25
        threshold = np.mean(S_db, axis=1) - Z_SCALE * np.std(S_db, axis=1)

        S_db[ S_db >= threshold[..., np.newaxis] ] = 1

    # shape du spectrogram est (n_mels, n_frames)
    # n_frames represente le temps
    return S_db

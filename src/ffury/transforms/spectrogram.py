from librosa import power_to_db
from librosa.feature import melspectrogram
from numpy import (
    max as np_max,
    min as np_min
)
from numpy.typing import NDArray
from sklearn.preprocessing import MinMaxScaler

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
    
    audio, sampling_rate = waveform_apply_config(audio, 
                                                 sampling_rate,
                                                 config)

    S = melspectrogram(y=audio,
                       power=2,
                       sr=config.clip_sampling_rate_hz,
                       n_fft=config.spectrogram_n_ftt,
                       hop_length=config.spectrogram_hop_length,
                       n_mels=config.spectrogram_n_mels,
                       fmin=config.spectrogram_fmin,
                       fmax=config.spectrogram_fmax)

    S_db = power_to_db(S, ref=np_max)

    # normalisation
    S_db = MinMaxScaler().fit_transform(S_db)

    # shape du spectrogram est (n_mels, n_frames)
    # n_frames represente le temps
    return S_db

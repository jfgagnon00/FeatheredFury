from librosa import (
    load,
    power_to_db,
    resample,
    to_mono
)
from librosa.feature import melspectrogram
from numpy import max as np_max
from numpy.typing import NDArray

from ..configs import PreprocessConfig

def spectrogram_from_ndarray(audio: NDArray,
                             sampling_rate: int,
                             config: PreprocessConfig) -> NDArray:
    """
    # Genere melspectrogram de audio
    """
    if audio.shape[0] > 1:
        audio = to_mono(audio)

    if sampling_rate != config.clip_sampling_rate_hz:
        audio = resample(audio,
                         orig_sr=sampling_rate,
                         target_sr=config.clip_sampling_rate_hz)
        
    if config.spectrogram_stft_window_size_ms < config.spectrogram_stft_frame_size_ms:
        raise ValueError(f"spectrogram_stft_window_size_ms {config.spectrogram_stft_window_size_ms} < spectrogram_stft_frame_size_ms {config.spectrogram_stft_frame_size_ms}")

    S = melspectrogram(y=audio,
                       power=2,
                       sr=config.clip_sampling_rate_hz,
                       n_fft=config.spectrogram_n_ftt,
                       hop_length=config.spectrogram_hop_length,
                       n_mels=config.spectrogram_n_mels,
                       fmin=config.spectrogram_fmin,
                       fmax=config.spectrogram_fmax)

    S_db = power_to_db(S, ref=np_max)

    # shape du spectrogram est (n_mels, n_frames)
    # n_frames represente le temps
    return S_db

def spectrogram_from_file(audio_filename: str,
                          config: PreprocessConfig) ->  NDArray:
    # resampler fichier audio
    audio, sampling_rate = load(audio_filename, 
                                sr=config.clip_sampling_rate_hz)
    duration = len(audio) / sampling_rate
    expected = config.segment_size_ms / 1000

    if duration <= expected:
        # clip audio trop court par rapport a la taille attendu d'un segment
        raise ValueError(f"Audio clip too short - {duration}, expected {expected}")

    return spectrogram_from_ndarray(audio, 
                                    sampling_rate,
                                    config)
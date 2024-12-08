from librosa import (
    load,
    to_mono,
    resample,
)
from typing import Tuple
from numpy.typing import NDArray

from ..configs import PreprocessConfig

def waveform_from_file(audio_filename: str,
                       config: PreprocessConfig) ->  Tuple[NDArray, int]:
    """
    Load fichier audio
    """
    # resampler fichier audio
    audio, sampling_rate = load(audio_filename, 
                                sr=None,
                                mono=None)
    duration = len(audio) / sampling_rate
    expected_min = config.segment_size_ms / 1000

    if duration <= expected_min:
        # clip audio trop court par rapport a la taille attendu d'un segment
        raise ValueError(f"Audio clip too short - {duration}, expected {expected_min}")
    
    return audio, sampling_rate

def waveform_apply_config(audio: NDArray,
                          sampling_rate: int,
                          config: PreprocessConfig) -> Tuple[NDArray, int]:
    """
    S'assure que audio est mono et a le sampling rate demander 
    dans la config de preprocessing
    """
    if audio.shape[0] > 1:
        audio = to_mono(audio)

    if sampling_rate != config.clip_sampling_rate_hz:
        audio = resample(audio,
                         orig_sr=sampling_rate,
                         target_sr=config.clip_sampling_rate_hz)
        
    return audio, config.clip_sampling_rate_hz

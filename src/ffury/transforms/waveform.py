from librosa import (
    load,
    to_mono,
    resample,
)
from numpy.typing import NDArray

from ..configs import PreprocessConfig

def waveform_from_file(audio_filename: str,
                       config: PreprocessConfig) ->  NDArray:
    """
    Load fichier audio et s'assure qu'il soit mono et a le sampling rate 
    demander dans la config de preprocessing
    """
    # resampler fichier audio
    audio, sampling_rate = load(audio_filename, 
                                sr=config.clip_sampling_rate_hz,
                                mono=True)
    duration = len(audio) / sampling_rate
    expected_min = config.segment_size_ms / 1000

    if duration <= expected_min:
        # clip audio trop court par rapport a la taille attendu d'un segment
        raise ValueError(f"Audio clip too short - {duration}, expected {expected_min}")
    
    return audio, sampling_rate

def waveform_apply_config(audio: NDArray,
                          sampling_rate: int,
                          config: PreprocessConfig) -> NDArray:
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

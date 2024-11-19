from math import ceil
from ..yaml import YamlDeserializable


@YamlDeserializable
class SpectrogramConfig:
    """
    Encapsule les proprietes pour le mel-spectrogram
    """
    def __init__(self):
        self.clip_sampling_rate_hz = 0
        self.spectrogram_stft_window_size_ms = 0
        self.spectrogram_stft_frame_size_ms = 0
        self.spectrogram_fmin = 0
        self.spectrogram_fmax = 0
        self.spectrogram_n_mels = 0

    @property
    def spectrogram_n_ftt(self):
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_window_size_ms / 1000)

    @property
    def spectrogram_hop_length(self):
        # number of samples to hop to get 1 spectrogram element
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_frame_size_ms / 1000)

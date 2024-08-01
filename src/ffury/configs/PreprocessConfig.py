from math import ceil
from ..yaml import YamlDeserializable


@YamlDeserializable
class PreprocessConfig:
    """
    Encapsule les proprietes pour le preprocessing
    """
    def __init__(self):
        self.split_stratify_on = None
        self.split_train_size = 0.0
        self.split_test_size = 0.0
        self.clip_sampling_rate_hz = 0
        self.clip_segment_size_ms = 0
        self.clip_segment_hop_size_ms = 0
        self.spectrogram_stft_frame_size_ms = 0
        self.spectrogram_stft_window_size_ms = 0
        self.spectrogram_fmin = 0
        self.spectrogram_fmax = 0
        self.spectrogram_n_mels = 0

    @property
    def spectrogram_n_ftt(self):
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_window_size_ms / 1000)
    
    @property
    def spectrogram_hop_length(self):
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_frame_size_ms / 1000)
    
    @property
    def spectrogram_shape(self):
        return (1, # instance
                self.spectrogram_n_mels, # height
                ceil(self.clip_segment_size_ms / self.spectrogram_stft_frame_size_ms)) # width
    
    @property
    def segment_hop_length(self):
        return ceil(self.clip_sampling_rate_hz * self.clip_segment_hop_size_ms / 1000)
    
    @property
    def segment_length(self):
        return ceil(self.clip_sampling_rate_hz * self.clip_segment_size_ms / 1000)

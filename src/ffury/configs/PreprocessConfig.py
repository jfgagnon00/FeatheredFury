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
        # number of samples to hop to get 1 spectrogram element
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_frame_size_ms / 1000)
    
    @property
    def spectrogram_segment_length(self):
        return ceil(self.clip_segment_size_ms / self.spectrogram_stft_frame_size_ms)

    @property
    def spectrogram_segment_hop_length(self):
        # number of spectrogram elements to hop to get 1 clip segement hop
        return ceil(self.clip_segment_hop_size_ms / self.spectrogram_stft_frame_size_ms)

    @property
    def spectrogram_segment_shape(self):
        # comme on store nos donnes sous format hdf5 et qu'on doit ajouter
        # via l'axe 0, on met spectrogram_n_mels dans l'axe 1
        # c-a-d shape == (time, n_mels)
        return (self.spectrogram_segment_length, # width
                self.spectrogram_n_mels) # height
    
    @property
    def segment_hop_length(self):
        return ceil(self.clip_sampling_rate_hz * self.clip_segment_hop_size_ms / 1000)
    
    @property
    def segment_length(self):
        return ceil(self.clip_sampling_rate_hz * self.clip_segment_size_ms / 1000)

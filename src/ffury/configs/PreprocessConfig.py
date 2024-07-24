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
        self.spectrogram_stft_frame_size_ms = 0
        self.spectrogram_stft_window_size_ms = 0
        self.spectrogram_fmin = 0
        self.spectrogram_fmax = 0

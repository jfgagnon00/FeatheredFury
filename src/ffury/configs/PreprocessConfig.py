from math import ceil
from ..yaml import YamlDeserializable


@YamlDeserializable
class PreprocessConfig:
    """
    Encapsule les proprietes pour le preprocessing
    """
    def __init__(self):
        # parametres segment
        self.segment_size_ms = 0
        self.segment_overlap_size_ms = 0
        self.group_segment_count = 0
        self.group_count = 0

        # parametres mel-spectrogram
        self.clip_sampling_rate_hz = 0
        self.spectrogram_stft_window_size_ms = 0
        self.spectrogram_stft_frame_size_ms = 0
        self.spectrogram_fmin = 0
        self.spectrogram_fmax = 0
        self.spectrogram_n_mels = 0

        # train/test/validation split
        self.split_train_size = 0
        self.split_test_size = 0

    @property
    def spectrogram_n_ftt(self):
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_window_size_ms / 1000)

    @property
    def spectrogram_hop_length(self):
        # number of samples to hop to get 1 spectrogram element
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_frame_size_ms / 1000)

    def group_info(self):
        """
        Retourne tuple avec la quantite de frames du spectrograme necessaire 
        pour avoir (groupe_length, segment_length, hop_length)
        """
        # nombre de frames du spectrograme requis pour avoir 1 overlap
        overlap_frame_length = int(self.segment_overlap_size_ms / self.spectrogram_stft_frame_size_ms + 0.5)
        segment_frame_length = int(self.segment_size_ms / self.spectrogram_stft_frame_size_ms + 0.5)
        hop_frame_length = segment_frame_length - overlap_frame_length

        group_frame_length = (self.group_segment_count - 1) * hop_frame_length + segment_frame_length

        return group_frame_length, segment_frame_length, hop_frame_length

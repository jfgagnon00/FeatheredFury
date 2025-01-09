from math import ceil

from ..misc.md5 import md5_from_iterable
from ..yaml import YamlDeserializable


@YamlDeserializable
class PreprocessConfig:
    """
    Encapsule les proprietes pour le preprocessing
    """
    def __init__(self):
        # parametres segment/groupe audio
        self.segment_size_ms = 0
        self.segment_overlap_size_ms = 0
        self.group_segment_count = 0
        self.group_count = 0

        # parametres segmentation (automatique bird activity estimation)
        self.segmentation_size_ms = 0
        self.segmentation_sigma_scale = 0
        self.segmentation_content_ratio_threshold = 0
        self.segmentation_erosion_shape = (3, 3)
        self.segmentation_dilation_shape = (3, 3)

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
        self.split_train_random_state = 42
        self.split_test_random_state = 24

    @property
    def spectrogram_n_ftt(self):
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_window_size_ms / 1000)

    @property
    def spectrogram_hop_length(self):
        # number of samples to hop to get 1 spectrogram element
        return ceil(self.clip_sampling_rate_hz * self.spectrogram_stft_frame_size_ms / 1000)
    
    def split_sampling_md5(self):
        """
        Utilitaire pour avoir une signature sur les parametres de split/resampling
        """
        return md5_from_iterable([
            self.split_train_size,
            self.split_test_size,
            self.split_train_random_state,
            self.split_test_random_state,
            self.segment_size_ms,
            self.segment_overlap_size_ms,
            self.group_segment_count,
            self.group_count])

    def spectrogram_md5(self):
        """
        Utilitaire pour avoir une signature sur les parametres de spectrogram/segmentation
        """
        return md5_from_iterable([
            self.clip_sampling_rate_hz,
            self.spectrogram_stft_window_size_ms,
            self.spectrogram_stft_frame_size_ms,
            self.spectrogram_fmin,
            self.spectrogram_fmax,
            self.spectrogram_n_mels,
            self.segmentation_size_ms,
            self.segmentation_sigma_scale,
            self.segmentation_content_ratio_threshold,
            self.segmentation_erosion_shape[0], self.segmentation_erosion_shape[1],
            self.segmentation_dilation_shape[0], self.segmentation_dilation_shape[1]])

    def group_frame_infos(self):
        """
        Retourne tuple avec la quantite de frames du spectrograme necessaire 
        pour avoir (groupe_length, segment_length, groupe_hop_length)
        """
        # nombre de frames du spectrograme requis pour avoir 1 overlap
        overlap_frame_length = int(self.segment_overlap_size_ms / self.spectrogram_stft_frame_size_ms + 0.5)
        segment_frame_length = int(self.segment_size_ms / self.spectrogram_stft_frame_size_ms + 0.5)
        group_hop_frame_length = segment_frame_length - overlap_frame_length

        group_frame_length = (self.group_segment_count - 1) * group_hop_frame_length + segment_frame_length

        return group_frame_length, segment_frame_length, group_hop_frame_length

    def group_ms_infos(self):
        """
        Retourne tuple avec la quantite de ms necessaire 
        pour avoir (groupe_length, segment_length, groupe_hop_ms_length)
        """
        assert self.segment_overlap_size_ms < self.segment_size_ms

        group_hop_ms_length = self.segment_size_ms - self.segment_overlap_size_ms
        group_ms_length = (self.group_segment_count - 1) * group_hop_ms_length + self.segment_size_ms

        return group_ms_length, self.segment_size_ms, group_hop_ms_length
    
    def train_input_shape(self):
        """
        Retourne la shape a utiliser comme input a une reseau de neuronnes.
        """
        _, segment_frame_length, _ = self.group_frame_infos()
        return self.group_segment_count, self.spectrogram_n_mels, segment_frame_length

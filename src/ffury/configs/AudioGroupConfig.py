from ..yaml import YamlDeserializable


@YamlDeserializable
class AudioGroupConfig:
    """
    Encapsule les proprietes des groupes/segments audio
    """
    def __init__(self):
        self.segment_size_ms = 0
        self.segment_overlap_size_ms = 0
        self.group_segment_count = 0
        self.group_count = 0

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

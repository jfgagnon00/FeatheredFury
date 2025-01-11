import numpy as np

from ffury.configs import PreprocessConfig
from librosa import mel_frequencies
from librosa.util import frame as rosa_frame
from numpy.typing import NDArray
from scipy.ndimage import (
    grey_dilation,
    grey_erosion
)


def mask_from_spectrogram(spectrogram: NDArray,
                          config: PreprocessConfig) -> NDArray:
    """
    # Genere un masque pour le spectrograme. 1 element par frame ou
    1 == frame contient chant oiseau et 0 == frame NE CONTIENT PAS de chant oiseau.
    Le masque est un estime tres peu precis.
    """
    # validation parametres
    if config.segmentation_size_ms <= 0:
        raise ValueError(f"segmentation_size_ms {config.segmentation_size_ms} doit etre > 0")
    
    if config.segmentation_size_ms < config.spectrogram_stft_frame_size_ms:
        raise ValueError(f"segmentation_size_ms {config.segmentation_size_ms} <= spectrogram_stft_frame_size_ms {config.spectrogram_stft_frame_size_ms}")

    if config.segmentation_sigma_scale <= 0:
        raise ValueError(f"segmentation_sigma_scale {config.segmentation_sigma_scale} doit etre > 0")

    # TODO: mettre spectrogram en valeur positive
    spectrogram = spectrogram + 1

    spec_min = np.min(spectrogram)
    spec_min = np.round(spec_min, 2)

    spec_max = np.max(spectrogram)
    spec_max = np.round(spec_max, 2)
    if spec_min < 0 or spec_max > 1:
        raise ValueError(f"spectrogram min et max ne semble pas dans l'interval [0, 1] - {spec_min}, {spec_max}")

    # recuperer la partie du spectrogram qui correspond aux frequences d'interet
    freqs = mel_frequencies(n_mels=config.spectrogram_n_mels,
                            fmin=config.spectrogram_fmin,
                            fmax=config.spectrogram_fmax)
    freqs_low_index = np.argwhere(freqs >= config.segmentation_fmin)[0][0]
    freqs_high_index = np.argwhere(freqs <= config.segmentation_fmax)[-1][0]
    spectrogram = spectrogram[ freqs_low_index:freqs_high_index, :]

    # decouper spectrogram en segments
    num_frames = int(config.segmentation_size_ms / config.spectrogram_stft_frame_size_ms)
    segments = rosa_frame(spectrogram,
                          frame_length=num_frames,
                          hop_length=num_frames)

    mask = np.zeros(spectrogram.shape[1], dtype=np.uint8)

    # appliquer la segmentation sur chaque segment
    for s, f in enumerate(range(segments.shape[-1])):
        segment_index = s * num_frames
        segment_mask = segmentation(segments[..., f], config)
        mask[segment_index:segment_index + num_frames] = segment_mask

    return mask

def segmentation(segment_data: NDArray, 
                 config: PreprocessConfig) -> NDArray:
    # filtre a travers les frames (temps)
    mu = np.mean(segment_data, axis=1, keepdims=True)
    sigma = np.std(segment_data, axis=1, keepdims=True)

    # threshold
    segment_data = segment_data - (mu + config.segmentation_sigma_scale * sigma)

    # binarize
    segment_data[segment_data < 0] = 0
    segment_data[segment_data > 0] = 1

    # enleve les petits morceaux isoles
    segment_data = grey_erosion(segment_data, config.segmentation_erosion_shape)
    segment_data = grey_dilation(segment_data, config.segmentation_dilation_shape)

    # binarize
    segment_data[segment_data < 0] = 0
    segment_data[segment_data > 0] = 1

    # marquer chaque frame ou il y a au moins 
    # 1 element dans l'axe des frequences
    mask = np.zeros(segment_data.shape[1], dtype=np.uint8)
    mask[ np.any(segment_data, axis=0) ] = 1

    return mask

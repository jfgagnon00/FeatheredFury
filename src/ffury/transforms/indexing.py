from h5py import (
    VirtualLayout, 
    VirtualSource
)
from numpy import (
    int32,
    float32
)
from numpy.typing import NDArray
from pandas import (
    DataFrame,
)
from pathlib import Path

from .properties import (
    _DURATION_MS,
    _FILENAME,
    _GROUP_BEGIN_MS,
    _LATITUDE,
    _LONGITUDE,
    _SPECIE,
    _SPECTROGRAM_GROUPS,
    _SPECTROGRAM,
)

from ..configs import ProjectConfig
from ..misc.hdf5 import open_file


def write_hdf5_dataset(hdf5_filename: str,
                       dataset: str,
                       data: NDArray) -> None:
    filename = Path(hdf5_filename)
    filename.parent.mkdir(exist_ok=True, parents=True)

    with open_file(filename, "w") as hdf5_file:
        hdf5_file.create_dataset(dataset, 
                                 data=data)
        hdf5_file.flush()

def write_hdf5_groups(hdf5_filename: str,
                      data_df: DataFrame,
                      config: ProjectConfig,
                      log_debug_info=False) -> None:
    hdf5_filename = Path(hdf5_filename)
    hdf5_filename.parent.mkdir(exist_ok=True, parents=True)
    with open_file(hdf5_filename, "w") as hdf5_file:
        hdf5_file.create_dataset(_LATITUDE,
                                 data=data_df[_LATITUDE].astype(float32))
        
        hdf5_file.create_dataset(_LONGITUDE,
                                 data=data_df[_LONGITUDE].astype(float32))
        
        hdf5_file.create_dataset(_SPECIE,
                                 data=data_df[_SPECIE].astype(int32))
        
        _, \
            segment_frame_length, \
            group_hop_frame_length = config.preprocess.group_frame_infos()

        # batch, n_segments, n_mels, n_frames)
        group_shape = (data_df.shape[0],
                       config.preprocess.group_segment_count, 
                       config.preprocess.spectrogram_n_mels,
                       segment_frame_length)
        
        # les groupes sont des vues sur d'autres fichiers hdf5
        # d'ou VirtualLayout et create_virtual_dataset
        group_layout = VirtualLayout(shape=group_shape,
                                     dtype=float32)
        
        for g in range(0, data_df.shape[0]):
            r = data_df.iloc[g]

            hdf5_source = Path.joinpath(config.paths.BUILD_DIR, _SPECTROGRAM, r[_FILENAME])
            hdf5_source = hdf5_source.with_suffix(".hdf5")

            spectrogram_frame_length = r[_DURATION_MS] / config.preprocess.spectrogram_stft_frame_size_ms
            spectrogram_frame_length = int(spectrogram_frame_length + 0.5) + 1

            source = VirtualSource(hdf5_source,
                                   _SPECTROGRAM,
                                   (config.preprocess.spectrogram_n_mels, spectrogram_frame_length),
                                   dtype=float32)

            segment_frame_begin = r[_GROUP_BEGIN_MS] / config.preprocess.spectrogram_stft_frame_size_ms
            segment_frame_begin = int(segment_frame_begin)

            if log_debug_info:
                print(hdf5_filename)

            for s in range(config.preprocess.group_segment_count):
                segment_frame_end = segment_frame_begin + segment_frame_length

                # validation non debordement
                assert segment_frame_end <= spectrogram_frame_length

                if log_debug_info:
                    print("    ", str(hdf5_source), g, s, (segment_frame_begin, segment_frame_end))

                group_layout[g, s, ...] = source[..., segment_frame_begin:segment_frame_end]
                segment_frame_begin += group_hop_frame_length

        hdf5_file.create_virtual_dataset(_SPECTROGRAM_GROUPS, group_layout)
        hdf5_file.flush()

def _md5_filename(config: ProjectConfig) -> str:
    return Path.joinpath(config.paths.BUILD_DIR, "data_indexed.md5")

def write_indexing_md5(config: ProjectConfig) -> str:
    filename = _md5_filename(config)
    with open(filename, "w") as file:
        print(config.preprocess.spectrogram_md5(), 
              file=file)

def read_indexing_md5(config: ProjectConfig) -> str:
    filename = _md5_filename(config)
    with open(filename, "r") as file:
        return file.read().strip()

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
    _GROUP_BEGIN,
    _SEGMENT_FRAME_LENGTH,
    _GROUP_HOP_FRAME_LENGTH,
    _FILENAME,
    _LATITUDE,
    _LONGITUDE,
    _MELSPECTROGRAM,
    _MELSPECTROGRAM_GROUPS,
    _SPECIE,
)

from ..configs import ProjectConfig
from ..dataset.hdf5 import open_file


def write_hdf5_dataset(hdf5_filename: str,
                       dataset: str,
                       data: NDArray) -> None:
    filename = Path(hdf5_filename)
    filename.parent.mkdir(exist_ok=True, parents=True)

    with open_file(filename, "w") as hdf5_file:
        hdf5_file.create_dataset(dataset, 
                                 data=data,
                                 compression="gzip")
        hdf5_file.flush()

def write_hdf5_groups(hdf5_filename: str,
                      data_df: DataFrame,
                      config: ProjectConfig) -> None:
    hdf5_filename = Path(hdf5_filename)
    hdf5_filename.parent.mkdir(exist_ok=True, parents=True)
    with open_file(hdf5_filename, "w") as hdf5_file:
        hdf5_file.create_dataset(_LATITUDE,
                                 data=data_df[_LATITUDE].astype(float32))
        
        hdf5_file.create_dataset(_LONGITUDE,
                                 data=data_df[_LONGITUDE].astype(float32))
        
        hdf5_file.create_dataset(_SPECIE,
                                 data=data_df[_SPECIE].astype(int32))

        # batch, n_segments, n_mels, n_frames)
        group_shape = (data_df.shape[0],
                       config.preprocess.group_segment_count, 
                       config.preprocess.spectrogram_n_mels,
                       data_df.iloc[0].segment_frame_length)
        
        # les groupes sont des vues sur d'autres fichiers hdf5
        # d'ou VirtualLayout et create_virtual_dataset
        group_layout = VirtualLayout(shape=group_shape,
                                     dtype=float32)
        
        for g in range(0, data_df.shape[0]):
            r = data_df.iloc[g]

            filename = Path.joinpath(config.paths.BUILD_DIR, _MELSPECTROGRAM, r[_FILENAME])
            filename = Path(filename).with_suffix(".hdf5")

            source = VirtualSource(filename, 
                                   _MELSPECTROGRAM,
                                   (config.preprocess.spectrogram_n_mels, r.spectrogram_frame_length),
                                   dtype=float32)

            segment_begin = r[_GROUP_BEGIN]
            for s in range(config.preprocess.group_segment_count):
                segment_end = segment_begin + r[_SEGMENT_FRAME_LENGTH]
                group_layout[g, s, ...] = source[..., segment_begin:segment_end]
                segment_begin += r[_GROUP_HOP_FRAME_LENGTH]

        hdf5_file.create_virtual_dataset(_MELSPECTROGRAM_GROUPS, group_layout)
        hdf5_file.flush()

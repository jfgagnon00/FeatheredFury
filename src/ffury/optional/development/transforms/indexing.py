from h5py import (
    VirtualLayout, 
    VirtualSource
)
from numpy import (
    float32,
    int16,
    uint8,
    copy,
    max,
    mean,
)
from numpy import eye
from numpy.typing import NDArray
from pandas import DataFrame
from pathlib import Path
from typing import Dict

from ffury.configs import ProjectConfig

from .properties import (
    _DURATION_MS,
    _FILENAME,
    _GROUP_BEGIN_MS,
    _LATITUDE,
    _LONGITUDE,
    _SPECIE,
    _SPECIE_ORIGINAL,
    _SPECTROGRAM,
    _SPECTROGRAM_MASK,
    _SPECTROGRAM_GROUPS,
    _SPECTROGRAM_MASK_GROUPS,
)
from ..misc.hdf5 import open_file


def write_hdf5_dataset(hdf5_filename: str,
                       datasets: Dict[str, NDArray]) -> None:
    filename = Path(hdf5_filename)
    filename.parent.mkdir(exist_ok=True, parents=True)

    with open_file(filename, "w") as hdf5_file:
        for name, data in datasets.items():
            hdf5_file.create_dataset(name=name,
                                     data=data)
        hdf5_file.flush()

def write_hdf5_groups(hdf5_filename: str,
                      data_df: DataFrame,
                      project_config: ProjectConfig,
                      log_debug_info=False) -> None:
    """
    Ecriture des groupes sous format hdf5. Voir jupyter notebooks pour 
    comprendre ce qu'est un groupe. 
    
    Note:
    Les spectrogrammes sont reference via un VirtualLayout afin de d'eliminer
    la redondance des donnees et simplifier le loading lors de l'entrainement.
    """
    hdf5_filename = Path(hdf5_filename)
    hdf5_filename.parent.mkdir(exist_ok=True, parents=True)
    with open_file(hdf5_filename, "w") as hdf5_file:
        hdf5_file.create_dataset(_LATITUDE,
                                 data=data_df[_LATITUDE].astype(float32))
        
        hdf5_file.create_dataset(_LONGITUDE,
                                 data=data_df[_LONGITUDE].astype(float32))

        # one hot encode _SPECIE_ORIGINAL
        # 1. Une classe de plus que ce qui est indique dans la config => classe Unknown
        # 2. Les masques ne sont pas encore calcule a cette etape. On garde les donnees
        #    d'origine ; permet validation a posteriori 
        I = eye(project_config.num_classes + 1, dtype=int16)
        hdf5_file.create_dataset(_SPECIE_ORIGINAL, 
                                 data=I[ data_df[_SPECIE] ])

        group_length, \
            segment_frame_length, \
            group_hop_frame_length = project_config.preprocess.group_frame_infos()

        # batch, n_segments, n_mels, n_frames)
        group_shape = (data_df.shape[0],
                       project_config.preprocess.group_segment_count, 
                       project_config.preprocess.spectrogram_n_mels,
                       segment_frame_length)

        mask_group_shape = (data_df.shape[0],
                            project_config.preprocess.group_segment_count, 
                            segment_frame_length)

        if log_debug_info:
            print(f"Groupe ms info: {project_config.preprocess.group_ms_infos()}")
            print(f"Groupe length frames: {group_length}")
            print(f"Groupe shape: {group_shape}")
            print(f"Groupe mask shape: {group_shape}")
        
        # les groupes sont des vues sur d'autres fichiers hdf5
        # d'ou VirtualLayout et create_virtual_dataset
        spectrogram_group_layout = VirtualLayout(shape=group_shape,
                                                 dtype=float32)
        spectrogram_mask_group_layout = VirtualLayout(shape=mask_group_shape,
                                                      dtype=uint8)
        
        for g in range(0, data_df.shape[0]):
            r = data_df.iloc[g]

            hdf5_source = Path.joinpath(project_config.paths.BUILD_DIR, _SPECTROGRAM, r[_FILENAME])
            hdf5_source = hdf5_source.with_suffix(".hdf5")

            spectrogram_frame_length = r[_DURATION_MS] / project_config.preprocess.spectrogram_stft_frame_size_ms
            spectrogram_frame_length = int(spectrogram_frame_length + 0.5) + 1

            spectrogram_source = VirtualSource(hdf5_source,
                                               _SPECTROGRAM,
                                               (project_config.preprocess.spectrogram_n_mels, spectrogram_frame_length),
                                               dtype=float32)

            spectrogram_mask_source = VirtualSource(hdf5_source,
                                                    _SPECTROGRAM_MASK,
                                                    spectrogram_frame_length,
                                                    dtype=uint8)

            segment_frame_begin = r[_GROUP_BEGIN_MS] / project_config.preprocess.spectrogram_stft_frame_size_ms
            segment_frame_begin = int(segment_frame_begin)

            if log_debug_info:
                print(f"Src: {hdf5_source}, {r[_GROUP_BEGIN_MS]}, {r[_DURATION_MS]}, {(project_config.preprocess.spectrogram_n_mels, spectrogram_frame_length)}")
                print(f"Dst: {hdf5_filename}")

            for s in range(project_config.preprocess.group_segment_count):
                segment_frame_end = segment_frame_begin + segment_frame_length

                # validation non debordement
                assert segment_frame_end <= spectrogram_frame_length, f"Debordement: {(segment_frame_begin,segment_frame_end)}"

                if log_debug_info:
                    print(f"    {str(hdf5_source)}, {g}, {s}, {(segment_frame_begin, segment_frame_end)}")

                spectrogram_group_layout[g, s, ...] = spectrogram_source[..., segment_frame_begin:segment_frame_end]
                spectrogram_mask_group_layout[g, s, ...] = spectrogram_mask_source[segment_frame_begin:segment_frame_end]

                segment_frame_begin += group_hop_frame_length

            if log_debug_info:
                # ligne vide entre groupes, facilite lecture des logs
                print()

        hdf5_file.create_virtual_dataset(_SPECTROGRAM_GROUPS, spectrogram_group_layout)
        hdf5_file.create_virtual_dataset(_SPECTROGRAM_MASK_GROUPS, spectrogram_mask_group_layout)
        hdf5_file.flush()

def update_hdf5_groups_labels(hdf5_filename: str,
                              project_config: ProjectConfig) -> None:
    # ouvrir hdf5_filename en mode update
    # on doit lire les masques et les labels pour mettre a jour ces derniers
    with open_file(hdf5_filename, "r") as hdf5_file:
        spectrogram_mask = hdf5_file[_SPECTROGRAM_MASK_GROUPS]

        # pourcentage de frames contenant chant d'oiseaum par segment
        segments_mask_ratio = mean(spectrogram_mask, axis=-1)

        # pourcentage de frames contenant chant d'oiseaum par groupe (le meilleur segment)
        groups_ratio = max(segments_mask_ratio, axis=-1)

        # si le meilleur segment d'un groupe est en dessous d'un seuil
        # forcer le label unknown
        group_audio_unavailable = groups_ratio < project_config.preprocess.segmentation_content_ratio_threshold

        # copy labels
        y = hdf5_file[_SPECIE_ORIGINAL][:]

        # sanity check
        assert y.shape[0] == spectrogram_mask.shape[0]
        assert y.shape[1] == project_config.num_classes + 1

    # classe unknown one hot enocded
    unknown_ohe = [0] * (project_config.num_classes + 1)
    unknown_ohe[-1] = 1

    with open_file(hdf5_filename, "r+") as hdf5_file:
        y[group_audio_unavailable] = unknown_ohe
        hdf5_file.create_dataset(_SPECIE,
                                 data=y)
        hdf5_file.flush()

def _md5_filename(project_config: ProjectConfig) -> str:
    return Path.joinpath(project_config.paths.BUILD_DIR, "data_indexed.md5")

def write_indexing_md5(project_config: ProjectConfig) -> str:
    filename = _md5_filename(project_config)
    with open(filename, "w") as file:
        print(project_config.preprocess.spectrogram_md5(), 
              file=file)

def read_indexing_md5(project_config: ProjectConfig) -> str:
    filename = _md5_filename(project_config)
    with open(filename, "r") as file:
        return file.read().strip()

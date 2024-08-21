import click

from dask.distributed import (
    as_completed,
    wait
)
from h5py import (
    Dataset,
    File,
    VirtualLayout, 
    VirtualSource
)
from logging import Logger
from librosa import load
from numpy import (
    array,
    int32,
    float32
)
from numpy.typing import NDArray
from pandas import (
    DataFrame,
    read_csv
)
from pathlib import Path
from tqdm import tqdm
from typing import (
    List,
    Union
)

from . import ProjectConfigDecorator
from .dataset import dataset_group
from ..configs import (
    DatasetType,
    load_config,
    PreprocessConfig,
    ProjectConfig,
)
from ..dataset.hdf5 import (
    open_file,
    join_keys
)
from ..dataset.preprocess import (
    get_num_segments,
    generate_segments,
    generate_spectrogram,
    generate_species_groups,
    _MELSPECTROGRAM_SEGMENT,
    _MELSPECTROGRAM,
    _SPECIES_CSV,
    _FILENAME,
    _LONGITUDE,
    _LATITUDE,
    _SPECIE
)
from ..misc.concurrent import create_dask_local_client
from ..misc.logging import create_logger


@dataset_group.command()
@click.option("--config", 
              type=click.Path(exists=True), 
              default=None,
              help="Override preprocess config")
@ProjectConfigDecorator
def preprocess(project_config: ProjectConfig, 
               config: str) -> None:
    """
    Encapsule preprocess du dataset (creation spectrograms + sauvegarde HDF5)
    """
    logger = create_logger(file=__file__)

    if not config is None:
        logger.info(f"Override preprocess config: '{config}'")
        project_config.preprocess = load_config(config)

    # charger data explore
    filename = project_config.get_csv_filename(DatasetType.EXPLORED)
    data_df = _load(logger, filename)

    # generer information par espece oiseau
    species_groups, species_str, species_categories = generate_species_groups(data_df)

    # estime count pour progress bar
    count = 1
    for _, specie_infos in species_groups:
        count += len(specie_infos)

    hdf5_segments_filename = Path.joinpath(project_config.paths.DATA_DIR, 
                                           "data_segments.hdf5")
    hdf5_segments_filename.parent.mkdir(exist_ok=True, parents=True)
    _init_segments_hdf5(hdf5_segments_filename)

    # traiter en parallele les donnees
    with tqdm(total=count) as progress:
        with create_dask_local_client(memory_limit="2GB") as client:
            writer_futures = []
            spectrogram_futures = []
            segment_futures = []

            filename = Path.joinpath(project_config.paths.DATA_DIR, 
                                     _SPECIES_CSV)
            future = client.submit(_write_species_str,
                                   species_str,
                                   filename)
            writer_futures.append(future)
            
            # 1 espece d'oiseau a la fois; minimise la quantite de fichiers sur disque
            # et ne surchage pas les capacites d'execution
            for specie_str, specie_infos in species_groups:
                specie_code = species_categories.get_loc(specie_str)

                for _, infos in specie_infos.iterrows():
                    filename = infos[_FILENAME]
                    latitude = infos[_LATITUDE]
                    longitude = infos[_LONGITUDE]
                    future = client.submit(_generate_spectrogram,
                                           project_config.get_audio_filename(filename),
                                           filename,
                                           latitude,
                                           longitude,
                                           specie_code,
                                           project_config.preprocess)
                    spectrogram_futures.append(future)

                # attendre que les dernieres ecritures soient terminee
                # hdf5_segments_filename ne peut etre ecrit que par 1 thread/process
                _wait_progress(writer_futures, progress)
                writer_futures.clear()

                # interleave generation spectrogram avec ecriture sur disque
                future = client.submit(_write_hdf5,
                                       hdf5_segments_filename,
                                       Path.joinpath(project_config.paths.DATA_DIR,
                                                     _MELSPECTROGRAM,
                                                     f"{specie_str}.hdf5"),
                                       project_config.preprocess,
                                       spectrogram_futures)
                writer_futures.append(future)
                segment_futures.append(future)

                # ne pas surcharger le scheduler ni le footprint memoire
                # chaque spectrogram est relativement long a faire dans tous les cas
                _wait_progress(spectrogram_futures, progress)
                spectrogram_futures.clear()

            # attendre que la derniere ecriture soit faite
            _wait_progress(writer_futures, progress)

            # completer ecriture segments (hdfs5 virtual dataset)
            for s in segment_futures:
                # print( s.result() )
                pass


def _wait_progress(futures, 
                   progress: tqdm) -> None:
    for f in as_completed(futures):
        progress.update()

def _load(logger: Logger, 
          filename: str) -> DataFrame:
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"{data_df.shape[0]} elements")
    return data_df

def _write_species_str(species_str: DataFrame,
                       filename: str) -> NDArray:
    filename = Path(filename)
    filename.parent.mkdir(exist_ok=True, parents=True)
    species_str.to_csv(filename, index=False)

def _generate_spectrogram(audio_filename: str,
                          filename: str,
                          latitude: float,
                          longitude: float,
                          specie_code: int,
                          config: PreprocessConfig) -> tuple[str, 
                                                             float, 
                                                             float, 
                                                             int, 
                                                             NDArray]:
    audio, sampling_rate = load(audio_filename)

    spectrogram = generate_spectrogram(audio, 
                                       sampling_rate,
                                       config)
    
    duration = len(audio) / sampling_rate
    ll = spectrogram.shape[0]

    if duration <= (config.clip_segment_size_ms / 1000):
        raise ValueError(f"Too short - {duration}, {ll}")

    return filename, \
           latitude, \
           longitude, \
           specie_code, \
           spectrogram

def _init_segments_hdf5(segments_filename: str):
    with open_file(segments_filename, "w") as hdf5_file:
        hdf5_file.create_dataset(_LATITUDE,
                                 # batch, latitude
                                 shape=(0, 1),
                                 dtype=float32,
                                 maxshape=(None, 1))
        
        hdf5_file.create_dataset(_LONGITUDE,
                                 # batch, longitude
                                 shape=(0, 1),
                                 dtype=float32,
                                 maxshape=(None, 1))
        
        hdf5_file.create_dataset(_SPECIE,
                                 # batch, specie_code
                                 shape=(0, 1),
                                 dtype=int32,
                                 maxshape=(None, 1))

def _write_hdf5(segments_filename: str,
                spectrogram_filename: str,
                config: PreprocessConfig,
                infos: List[tuple[str, float, float, int, NDArray]]) -> None:
    spectrogram_filename = Path(spectrogram_filename)
    spectrogram_filename.parent.mkdir(exist_ok=True, parents=True)

    layouts = []

    with open_file(segments_filename, "a") as hdf5_segments:
        with open_file(spectrogram_filename, "w") as hdf5_spectrogram:
            for filename, latitude, longitude, specie_code, spectrogram in infos:
                hdf5_spectrogram.create_dataset(filename, 
                                                data=spectrogram)

                _append_spectrogram_segments(hdf5_segments,
                                             latitude, 
                                             longitude, 
                                             specie_code,
                                             spectrogram.shape[0],
                                             config)

                layouts.append((spectrogram_filename, filename, spectrogram.shape[0]))

            hdf5_spectrogram.flush()
        hdf5_segments.flush()

    return layouts

def _append_spectrogram_segments(hdf5_file: File,
                                 latitude: float,
                                 longitude: float,
                                 specie_code: int, 
                                 spectrogram_length: int,
                                 config: PreprocessConfig) -> None:
    segments_count = get_num_segments(spectrogram_length, config)

    if segments_count == 0:
        raise ValueError(f"Segment count == 0; {spectrogram_length}, {config.spectrogram_segment_hop_length}")
    
    # segments_shape = config.spectrogram_segment_shape

    # segments_source = VirtualSource(spectrogram_filename, 
    #                                 spectrogram_name,
    #                                 spectrogram_shape,
    #                                 dtype=float32)

    # segments_layout = VirtualLayout(# batch, time, n_mels
    #                                 shape=(0, *segments_shape),
    #                                 dtype=float32,
    #                                 maxshape=(None, *segments_shape))

    # for start, end in generate_segments(spectrogram_shape[0], config):
    #     segments_count += 1
    #     segments_layout.shape = (segments_count, *segments_shape)
    #     segments_layout[segments_count - 1, ...] = segments_source[start:end, ...]

    _append(hdf5_file[_LATITUDE], 
            latitude, 
            float32, 
            segments_count)
    
    _append(hdf5_file[_LONGITUDE], 
            longitude, 
            float32, 
            segments_count)
    
    _append(hdf5_file[_SPECIE], 
            specie_code, 
            int32, 
            segments_count)

def _append(dataset: Dataset, 
            data: Union[int, float],
            dtype: Union[int32, float32],
            num_segments: int) -> None:
    shape = list(dataset.shape)
    shape[0] += num_segments
    dataset.resize(shape)

    data = array([data] * num_segments, dtype=dtype)
    dataset[-num_segments:] = data.reshape((num_segments, -1))

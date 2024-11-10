import click

from dask.distributed import (
    as_completed,
    wait
)
from h5py import (
    Dataset,
    VirtualLayout, 
    VirtualSource
)
from itertools import islice
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
    read_csv,
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
)
from ..dataset.preprocess import (
    generate_spectrogram,
    generate_species_groups,
    _MELSPECTROGRAM_GROUPS,
    _MELSPECTROGRAM,
    _SPECIES_CSV,
    _FILENAME,
    _LONGITUDE,
    _LATITUDE,
    _SPECIE
)
from ..misc.concurrent import create_dask_local_client
from ..misc.halton import halton_sequence
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
    Encapsule preprocess du dataset (creation spectrograms + sauvegarde HDF5 + split)
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

    tmp_filename = Path.joinpath(project_config.paths.BUILD_DIR, "data_temp.csv")
    tmp_filename.parent.mkdir(exist_ok=True, parents=True)

    logger.info(f"Creation spectrograms + information de groupe")

    # traiter en parallele les donnees
    with tqdm(total=count) as progress:
        with create_dask_local_client(memory_limit="2GB") as client:
            writer_futures = []
            spectrogram_futures = []
            write_header = True

            # ecrire dataset primary_label, common_name dans fichier .csv
            # plus simple que hdf5 et eviter le traitement des strings
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
                # groups_hdf5_filename ne peut etre ecrit que par 1 thread/process
                _wait_progress(writer_futures, progress)
                writer_futures.clear()

                # interleave generation spectrogram avec ecriture sur disque
                specie_hdf5_filename = Path.joinpath(project_config.paths.DATA_DIR,
                                                     _MELSPECTROGRAM,
                                                     f"{specie_str}.hdf5")
                future = client.submit(_write_specie_spectrogram,
                                       specie_hdf5_filename,
                                       spectrogram_futures)
                writer_futures.append(future)

                # resampler
                future = client.submit(_create_specie_groups,
                                       tmp_filename,
                                       write_header,
                                       specie_hdf5_filename,
                                       project_config.preprocess,
                                       future)
                writer_futures.append(future)

                # ne pas surcharger le scheduler ni le footprint memoire
                # chaque spectrogram est relativement long a faire dans tous les cas
                _wait_progress(spectrogram_futures, progress)
                spectrogram_futures.clear()

                write_header = False

            # attendre que la derniere ecriture soit faite
            _wait_progress(writer_futures, progress)

    logger.info(f"Creation des groupes")

    # creation du fichier final
    hdf5_groups_filename = Path.joinpath(project_config.paths.DATA_DIR, 
                                         "data_groups.hdf5")
    hdf5_groups_filename.parent.mkdir(exist_ok=True, parents=True)
    _create_hdf5_groups(tmp_filename,
                        hdf5_groups_filename,
                        project_config.preprocess)

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
    # resampler fichier audio
    audio, sampling_rate = load(audio_filename, 
                                sr=config.clip_sampling_rate_hz)
    duration = len(audio) / sampling_rate
    expected = config.segment_size_ms / 1000

    if duration <= expected:
        # clip audio trop court par rapport a la taille attendu d'un segment
        raise ValueError(f"Audio clip too short - {duration}, expected {expected}")

    spectrogram = generate_spectrogram(audio, 
                                       sampling_rate,
                                       config)

    return filename, \
           latitude, \
           longitude, \
           specie_code, \
           spectrogram

def _write_specie_spectrogram(spectrogram_filename: str,
                              infos: List[tuple[str, float, float, int, NDArray]]) -> \
                                List[tuple[str, float, float, int, NDArray]]:
    spectrogram_filename = Path(spectrogram_filename)
    spectrogram_filename.parent.mkdir(exist_ok=True, parents=True)

    layouts = []

    with open_file(spectrogram_filename, "w") as hdf5_spectrogram:
        for filename, latitude, longitude, specie_code, spectrogram in infos:
            hdf5_spectrogram.create_dataset(filename, 
                                            data=spectrogram)
            layouts.append((filename, 
                            latitude, 
                            longitude, 
                            specie_code,
                            spectrogram.shape))

        hdf5_spectrogram.flush()
    
    return layouts

def _create_hdf5_groups(temp_filename: str,
                        hdf5_filename: str,
                        config: PreprocessConfig):
    # TODO: sous performant et dangeureux - refaire quand le temps le permetra
    from ast import literal_eval

    data_df = read_csv(temp_filename)
    data_df["spectrogram_shape"] = data_df["spectrogram_shape"].apply(literal_eval)
    data_df["segments"] = data_df["segments"].apply(literal_eval)

    # cree des dataset vide ; la clef doit etre presente
    # avant d'ecrire les donnees (contrainte multiprocessing)
    with open_file(hdf5_filename, "w") as hdf5_file:
        hdf5_file.create_dataset(_LATITUDE,
                                 data=data_df["latitude"].astype(float32))
        
        hdf5_file.create_dataset(_LONGITUDE,
                                 data=data_df["longitude"].astype(float32))
        
        hdf5_file.create_dataset(_SPECIE,
                                 data=data_df["specie_code"].astype(int32))
        
        # les groupes sont des vues sur d'autres fichiers hdf5
        # d'ou VirtualLayout et create_virtual_dataset
        _, segment_frame_length, _ = config.group_info()
        group_shape = (data_df.shape[0],
                       config.group_segment_count, 
                       config.spectrogram_n_mels,
                       segment_frame_length)
        
        group_layout = VirtualLayout(# batch, n_segments, n_mels, n_frames)
                                     shape=group_shape,
                                     dtype=float32)
        
        for g, tuple_row in enumerate(data_df.iterrows()):
            r = tuple_row[1]
            source = VirtualSource(r["specie_hdf5_filename"], 
                                   r["specie_hdf5_dataset"],
                                   r["spectrogram_shape"],
                                   dtype=float32)
            for s, (segment_begin, segment_end) in enumerate(r["segments"]):
                group_layout[g, s, ...] = source[..., segment_begin:segment_end]
        
        hdf5_file.create_virtual_dataset(_MELSPECTROGRAM_GROUPS, group_layout)
        hdf5_file.flush()

def _create_specie_groups(temp_filename: str,
                          write_header: bool,
                          specie_hdf5_filename: str,
                          config: PreprocessConfig,
                          infos: List[tuple[str, float, float, int, tuple[int, int]]]) -> None:
    if config.group_count < 1:
        raise ValueError(f"group_count < 1: {config.group_count}")

    # construire array pour remapper nombre [0, 1] a index dans infos
    # doit tenir compte de spectrogram_length
    length = 0
    lengths = []
    for _, \
        _, \
        _, \
        _, \
        spectrogram_shape in infos:
        lengths.append((length, length + spectrogram_shape[1]))
        length += spectrogram_shape[1]

    # determiner la quantite de frames necessaire pour group, segment et hop
    _, \
        segment_frame_length, \
        group_hop_frame_length = config.group_info()

    group_datas = []
  
    for g in islice(halton_sequence(3), config.group_count):
        # ramapper [0, 1] a [0, length]
        group_begin = int(g * length)

        # trouver le fichier et la position dans le fichier qui 
        # correspond a group_begin
        for i, (begin, end) in enumerate(lengths):
            if end > group_begin:
                break
        group_begin = group_begin - begin

        group_data = {}

        # obtrenir les informations specifiques du fichier
        group_data["specie_hdf5_filename"] = specie_hdf5_filename
        group_data["specie_hdf5_dataset"], \
            group_data["latitude"], \
            group_data["longitude"], \
            group_data["specie_code"], \
            group_data["spectrogram_shape"] = infos[i]

        # segment => vue sur le data source specifie par 
        # specie_hdf5_filename et specie_hdf5_dataset
        segment_sources = []
        for s in range(config.group_segment_count):
            segment_begin = group_begin
            segment_end = group_begin + segment_frame_length

            if segment_end >= spectrogram_shape[1]:
                segment_end = spectrogram_shape[1]
                segment_begin = spectrogram_shape[1] - segment_frame_length

            segment_sources.append((segment_begin, segment_end))
            group_begin += group_hop_frame_length

        group_data["segments"] = segment_sources
        group_datas.append(group_data)

    # limitation hdf5 ; les dataset virtuels doivent etre creee en 1 seul etape
    # le resize n'est pas supporte
    group_df = DataFrame(group_datas)
    group_df.to_csv(temp_filename, 
                    mode="w" if write_header else "a", 
                    index=False,
                    header=write_header)

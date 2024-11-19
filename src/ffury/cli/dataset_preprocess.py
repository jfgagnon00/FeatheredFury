import click

from dask.distributed import as_completed
from pandas import read_csv
from pathlib import Path
from tqdm import tqdm

from . import ProjectConfigDecorator
from .dataset import dataset_group
from ..configs import (
    DatasetType,
    load_config,
    PreprocessConfig,
    ProjectConfig
)

from ..dataset.preprocess import (
    generate_species_groups,
    generate_specie_groups,
    write_hdf5_dataset,
    write_species_dataframe,
    split,
    write_hdf5_groups,
    _FILENAME,
    _MELSPECTROGRAM
)
from ..feature import spectrogram_from_file
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
    Encapsule preprocess du dataset (creation spectrograms + split)
    """
    logger = create_logger(file=__file__)

    if not config is None:
        logger.info(f"Override preprocess config: '{config}'")
        project_config.preprocess = load_config(config)

    # charger data explore
    filename = project_config.get_csv_filename(DatasetType.EXPLORED)
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"{data_df.shape[0]} elements")

    # generer information par espece oiseau
    species_groups, species_str, species_categories = generate_species_groups(data_df)

    # estime count pour progress bar
    # write_species_dataframe
    count = 1
    for _, specie_infos in species_groups:
        # write_species_dataframe
        count += 1

        # spectrogram_from_file + write_hdf5_dataset
        count += len(specie_infos) * 2

    logger.info(f"Creation spectrogrames + information de groupes")

    groups_df_filename = Path.joinpath(project_config.paths.BUILD_DIR, "groups.csv")
    groups_df_mode = "w"

    # traiter en parallele les donnees
    with tqdm(total=count) as progress:
        with create_dask_local_client(memory_limit="2GB") as client:
            previous_writer_futures = []
            current_writer_futures = []
            spectrogram_futures = []

            # ecrire dataset primary_label, common_name dans fichier .csv
            # plus simple que hdf5 et eviter le traitement des strings
            future = client.submit(write_species_dataframe,
                                   project_config.get_csv_filename(DatasetType._SPECIES),
                                   species_str)
            current_writer_futures.append(future)

            # 1 espece d'oiseau a la fois; minimise la quantite de fichiers sur disque
            # et ne surchage pas les capacites d'execution
            for specie_str, specie_infos in species_groups:
                # resampler l'audio en groupes (pas besoin du data en tant que tel)
                # puisque que des vues sont utilisees
                future = client.submit(generate_specie_groups,
                                       groups_df_filename,
                                       groups_df_mode,
                                       Path.joinpath(project_config.paths.DATA_DIR, _MELSPECTROGRAM),
                                       specie_infos,
                                       specie_str,
                                       species_categories.get_loc(specie_str),
                                       project_config.preprocess)
                current_writer_futures.append(future)

                for _, filename in specie_infos[_FILENAME].items():
                    # generer le spectrogram
                    future = client.submit(spectrogram_from_file,
                                           project_config.get_audio_filename(filename),
                                           project_config.preprocess)
                    spectrogram_futures.append(future)
                    
                    # ecrire le spectrogram
                    future = client.submit(write_hdf5_dataset,
                                           Path.joinpath(project_config.paths.DATA_DIR,
                                                         _MELSPECTROGRAM,
                                                         filename).with_suffix(".hdf5"),
                                           "w",
                                           _MELSPECTROGRAM,
                                           future)
                    current_writer_futures.append(future)

                # ne pas surcharger le scheduler ni le footprint memoire
                # chaque spectrogram est relativement long a faire dans tous les cas
                _wait_progress(spectrogram_futures, progress)
                spectrogram_futures.clear()

                _wait_progress(previous_writer_futures, progress)
                previous_writer_futures.clear()
                previous_writer_futures = current_writer_futures
                current_writer_futures = []

                groups_df_mode = "a"

            # attendre que la derniere ecriture soit faite
            _wait_progress(previous_writer_futures, progress)
            previous_writer_futures.clear()

    logger.info(f"Split")
    train_df, test_df, validation_df = split(groups_df_filename, 
                                             project_config.preprocess,
                                             logger)

    logger.info(f"Ecriture data train")
    write_hdf5_groups(project_config.get_hdf5_filename(DatasetType.TRAIN),
                      "w",
                      train_df,
                      project_config.preprocess)
    
    logger.info(f"Ecriture data test")
    write_hdf5_groups(project_config.get_hdf5_filename(DatasetType.TEST),
                      "w",
                      test_df,
                      project_config.preprocess)
    
    logger.info(f"Ecriture data validation")
    write_hdf5_groups(project_config.get_hdf5_filename(DatasetType.VALIDATION),
                      "w",
                      validation_df,
                      project_config.preprocess)

def _wait_progress(futures, 
                   progress: tqdm) -> None:
    for f in as_completed(futures):
        progress.update()

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

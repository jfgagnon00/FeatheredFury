import click

from dask.distributed import wait
from os import cpu_count
from pandas import read_csv
from pathlib import Path
from tqdm import tqdm

from ffury.cli import ProjectConfigDecorator
from ffury.configs import (
    DatasetType,
    ProjectConfig
)
from ffury.transforms import (
    spectrogram_from_audio,
    waveform_apply_config,
    waveform_from_file,
)
from ffury.misc.concurrent import create_dask_local_client
from ffury.misc.logging import create_logger

from .dataset import dataset_group
from ..transforms.properties import (
    _FILENAME,
    _SPECTROGRAM,
    _SPECTROGRAM_MASK
)
from ..transforms import (
    get_audio_path,
    mask_from_spectrogram,
    write_hdf5_dataset,
    write_hdf5_groups,
    write_indexing_md5
)


@dataset_group.command()
@click.option("--log-debug-info", 
              "log_debug_info", 
              is_flag=True, 
              default=False, 
              show_default=True, 
              help="Log debug info")
@ProjectConfigDecorator
def index(project_config: ProjectConfig,
          log_debug_info) -> None:
    """
    Genere les spectrogrames et index les ensembles train/test/validation
    """
    logger = create_logger(file=__file__)

    if log_debug_info:
        logger.info(f"log_debug_info active")

    # prendre en note les fichiers utilises
    # les spectrogrammes ne seront generes que pour ces fichiers
    filenames = set()

    for dataset_type in [DatasetType.TRAIN, DatasetType.TEST, DatasetType.VALIDATION]:
        logger.info(f"Indexation spectrograms '{dataset_type.name}'")
        dataset_df = read_csv(project_config.get_csv_filename(dataset_type))
        filenames.update( dataset_df[_FILENAME].unique() )
        write_hdf5_groups(project_config.get_hdf5_filename(dataset_type),
                          dataset_df, 
                          project_config,
                          log_debug_info=log_debug_info)

    logger.info(f"Creation spectrogrames + masques")

    # generer en parallele les spectrogrames
    with create_dask_local_client() as client:
        writer_futures = []

        for filename in tqdm(filenames):
            future = client.submit(waveform_from_file,
                                   Path.joinpath(get_audio_path(project_config.paths), 
                                                 filename),
                                   project_config.preprocess)

            future = client.submit(lambda future: waveform_apply_config(*future, project_config.preprocess),
                                   future)

            future_spectrogram = client.submit(lambda future: spectrogram_from_audio(*future, project_config.preprocess),
                                               future)

            future_spectrogram_mask = client.submit(lambda spec: mask_from_spectrogram(spec, project_config.preprocess),
                                                    future_spectrogram)

            hdf5_filename = Path.joinpath(project_config.paths.BUILD_DIR,
                                          _SPECTROGRAM,
                                          filename).with_suffix(".hdf5")
            future = client.submit(lambda spec, mask: write_hdf5_dataset(hdf5_filename, {_SPECTROGRAM:spec, _SPECTROGRAM_MASK: mask}),
                                   future_spectrogram,
                                   future_spectrogram_mask)

            writer_futures.append(future)

            # ne pas surgarger le systeme, attendre qu'un groupe de
            # traitements termine avant d'en lancer un autre
            # TODO: a refactorer - dask devrait s'en occuper
            if len(writer_futures) == (cpu_count() * 2):
                wait(writer_futures)
                writer_futures.clear()

        # attendre la fin des calcul de spectrogrames 
        # avant de les ecrires
        wait(writer_futures)

    # generer les vues sur les spectrogrammes + masques


    # prendre en note une signature des parametres utilises pour l'indexation
    logger.info(f"Ecriture signature md5")
    write_indexing_md5(project_config)

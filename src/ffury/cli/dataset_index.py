from dask.distributed import wait
from os import cpu_count
from pandas import read_csv
from pathlib import Path
from tqdm import tqdm

from . import ProjectConfigDecorator
from .dataset import dataset_group
from ..configs import (
    DatasetType,
    ProjectConfig
)

from ..transforms import (
    spectrogram_from_audio,
    waveform_apply_config,
    waveform_from_file,
    write_hdf5_dataset,
    write_hdf5_groups
)
from ..transforms.properties import (
    _FILENAME,
    _SPECTROGRAM
)
from ..misc.concurrent import create_dask_local_client
from ..misc.logging import create_logger


@dataset_group.command()
@ProjectConfigDecorator
def index(project_config: ProjectConfig) -> None:
    """
    Genere les spectrogrames et index les ensembles train/test/validation
    """
    logger = create_logger(file=__file__)

    filenames = set()

    for dataset_type in [DatasetType.TRAIN, DatasetType.TEST, DatasetType.VALIDATION]:
        logger.info(f"Indexation spectrograms '{dataset_type.name}'")
        dataset_df = read_csv(project_config.get_csv_filename(dataset_type))
        filenames.update( dataset_df[_FILENAME].unique() )
        write_hdf5_groups(project_config.get_hdf5_filename(dataset_type),
                          dataset_df, 
                          project_config)

    logger.info(f"Creation spectrogrames")

    # traiter en parallele les donnees
    with create_dask_local_client() as client:
        writer_futures = []

        for filename in tqdm(filenames):
            future = client.submit(waveform_from_file,
                                   project_config.get_audio_filename(filename),
                                   project_config.preprocess)

            future = client.submit(lambda future: waveform_apply_config(*future, project_config.preprocess),
                                   future)

            future = client.submit(lambda future: spectrogram_from_audio(*future, project_config.preprocess),
                                   future)

            hdf5_filename = Path.joinpath(project_config.paths.BUILD_DIR,
                                          _SPECTROGRAM,
                                          filename).with_suffix(".hdf5")
            future = client.submit(lambda future: write_hdf5_dataset(hdf5_filename, _SPECTROGRAM, future),
                                   future)

            writer_futures.append(future)

            if len(writer_futures) == (cpu_count() * 2):
                wait(writer_futures)
                writer_futures.clear()
        
        wait(writer_futures)

    # prendre en note une signature des parametres utilises pour l'indexation
    filename = Path.joinpath(project_config.paths.BUILD_DIR, "data_indexed.md5")
    logger.info(f"Ecriture '{filename}'")
    with open(filename, "w") as file:
        print(project_config.preprocess.spectrogram_md5(), 
              file=file)

import click

from logging import Logger
from librosa import load
from dask.distributed import (
    as_completed,
    Client
)
from numpy import save
from numpy.typing import NDArray
from pandas import (
    DataFrame,
    read_csv
)
from pathlib import Path
from tqdm import tqdm
from typing import List

from . import ProjectConfigDecorator
from .dataset import dataset_group
from ..configs import (
    DatasetType,
    load_config,
    PathsConfig,
    PreprocessConfig,
    ProjectConfig,
)
from ..dataset.preprocess import (
    generate_segment_spectrograms,
    generate_uinique_species,
    _MELSPECTROGRAM,
    _SPECIES_CSV,
    _FILENAME,
    _LONGITUDE,
    _LATITUDE,
    _SPECIE
)
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
    Encapsule preprocess du dataset (split + conversion HDF5)
    """
    logger = create_logger(file=__file__)

    if not config is None:
        logger.info(f"Override preprocess config: '{config}'")
        project_config.preprocess = load_config(config)

    # charger data explore
    filename = project_config.get_csv_filename(DatasetType.EXPLORED)
    data_df = _load(logger, filename)

    filename = project_config.get_csv_filename(DatasetType.PREPROCESS)
    _create_preprocessed_dataframe(filename)

    # generer dataframe pour noms et codes especes oiseaux
    species_codes = _preprocess_species(data_df, 
                                        project_config.paths)

    # traiter en parallele les donnees
    with Client() as client:
        tasks = []
        for index in range(data_df.shape[0]):
            row = data_df.iloc[index]

            # decouper chaque fichier audio en segments et calculer leurs spectrogrammes
            spectrograms = client.submit(_preprocess_audio_file,
                                         row[_FILENAME],
                                         project_config)

            # colliger resultats dans un dataframe
            update = client.submit(_update_preprocessed_dataframe,
                                   row[_LATITUDE], 
                                   row[_LONGITUDE], 
                                   species_codes[index],
                                   spectrograms,
                                   filename)
            

            tasks.append(update)

        with tqdm(total=len(tasks)) as progress:
            for task in as_completed(tasks):
                del task
                progress.update()

def _load(logger: Logger, 
          filename: str) -> DataFrame:
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"{data_df.shape[0]} elements")
    return data_df

def _preprocess_species(data: DataFrame,
                        config: PathsConfig) -> NDArray:
    species_str, species_codes = generate_uinique_species(data)

    filename = Path.joinpath(config.DATA_DIR, _SPECIES_CSV)
    filename.parent.mkdir(exist_ok=True, parents=True)
    species_str.to_csv(filename, index=False)
    return species_codes

def _preprocess_audio_file(input_filename: str,
                           config: ProjectConfig) -> List[str]:
    audio_filename = config.get_audio_filename(input_filename)
    spectrograms = _generate_segments(audio_filename, 
                                      config.preprocess)
    return _write_segments(input_filename, 
                           spectrograms,
                           config.paths)

def _generate_segments(input_filename: str,
                       config: PreprocessConfig) -> List[NDArray]:
    audio, sampling_rate = load(input_filename)
    return generate_segment_spectrograms(audio, 
                                         sampling_rate,
                                         config)

def _write_segments(input_filename: str, 
                    spectrograms: List[NDArray],
                    config: PathsConfig) -> List[str]:
    input_filename = Path(input_filename)
    relative_prefix = Path.joinpath(Path(_MELSPECTROGRAM),
                                    input_filename.parents[0])
    spectrogram_prefix = Path.joinpath(config.DATA_DIR,
                                       relative_prefix)
    spectrogram_prefix.mkdir(exist_ok=True, 
                             parents=True)

    spectrogram_filenames = []

    for i, S_db in enumerate(spectrograms):
        filename = f"{input_filename.stem}-{i:04d}.npy"
        save(spectrogram_prefix.joinpath(filename), S_db)

        spectrogram_filenames.append(relative_prefix.joinpath(filename))

    return spectrogram_filenames

def _create_preprocessed_dataframe(filename: str) -> None:
    dataframe = DataFrame(columns=[
        _MELSPECTROGRAM, 
        _LATITUDE, 
        _LONGITUDE, 
        _SPECIE])
    dataframe.to_csv(filename, index=False)

def _update_preprocessed_dataframe(latitude: float,
                                   longitude: float,
                                   specie: int,
                                   spectrograms: List[str],
                                   filename: str) -> None:
    count = len(spectrograms)
    dataframe = DataFrame({
        _MELSPECTROGRAM: spectrograms,
        _LATITUDE: [latitude] * count,
        _LONGITUDE: [longitude] * count,
        _SPECIE: [specie] * count
    })
    dataframe.to_csv(filename, 
                     mode="a+", 
                     index=False, 
                     header=False)

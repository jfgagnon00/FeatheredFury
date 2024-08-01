import click

from logging import Logger
from librosa import load
from joblib import (
    delayed,
    Parallel
)
from numpy import save
from numpy.typing import NDArray
from pandas import (
    read_csv, 
    DataFrame,
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
from ..dataset.preprocess import generate_segment_spectrograms
from ..misc.logging import create_logger

_MELSPECTROGRAM = "melspectrogram"


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
    
    # decouper chaque fichier audio en segments et calculer leurs spectrogrammes
    parallel = Parallel(n_jobs=-1, return_as="generator_unordered")
    preprocess_generator = parallel(delayed(_preprocess_file)(f, project_config) for f in data_df.loc[:20, "filename"])

    # pour afficher progres
    for _ in tqdm(preprocess_generator, total=data_df.shape[0]):
        pass

def _load(logger: Logger, 
          filename: str) -> DataFrame:
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"{data_df.shape[0]} elements")
    return data_df

def _preprocess_file(input_filename: str,
                     config: ProjectConfig) -> List[str]:
    audio_filename = config.get_audio_filename(input_filename)
    spectrograms = _generate_segments(audio_filename, 
                                      config.preprocess)
    return write_segments(input_filename, 
                          spectrograms,
                          config.paths)

def _generate_segments(input_filename: str,
                       config: PreprocessConfig) -> List[NDArray]:
    audio, sampling_rate = load(input_filename)
    return generate_segment_spectrograms(audio, 
                                         sampling_rate,
                                         config)

def write_segments(input_filename: str, 
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

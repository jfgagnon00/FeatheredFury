import pandas
import timeit

from ffury.configs import load_config
from ffury.dataset.preprocess import generate_segment_spectrograms
from joblib import (
    delayed,
    Parallel
)
from librosa import load
from librosa.feature import melspectrogram
from numpy import save
from numpy.typing import NDArray
from pathlib import Path
from tqdm import tqdm
from typing import List

_MELSPECTROGRAM = "melspectrogram"

project_config = load_config("/Users/jfgagnon/Projects/FeatheredFury/ffury.yaml")
data = pandas.read_csv("/Users/jfgagnon/Projects/FeatheredFury/data/data_explored.csv")

def produce_segments(input_filename: str) -> List[NDArray]:
    audio_filename = project_config.get_audio_filename(input_filename)
    audio, sampling_rate = load(audio_filename)
    return input_filename, \
           generate_segment_spectrograms(audio, 
                                         sampling_rate,
                                         project_config.preprocess)

def write_segments(input_filename: str, 
                   spectrograms: List[NDArray]) -> List[str]:
    input_filename = Path(input_filename)
    relative_prefix = Path.joinpath(Path(_MELSPECTROGRAM),
                                    input_filename.parents[0])
    spectrogram_prefix = Path.joinpath(project_config.paths.DATA_DIR,
                                       relative_prefix)
    spectrogram_prefix.mkdir(exist_ok=True, 
                             parents=True)
    
    spectrogram_filenames = []

    for i, S_db in enumerate(spectrograms):
        # sauvegarder spectrograms
        filename = f"{input_filename.stem}-{i:04d}.npy"
        save(spectrogram_prefix.joinpath(filename), S_db)

        # ajouter aux resultats
        spectrogram_filenames.append(relative_prefix.joinpath(filename))

    return spectrogram_filenames

def process_segments(input_filename: str) -> List[str]:
    filename, spectrograms = produce_segments(input_filename)
    return write_segments(filename, spectrograms)

def main_parallel(filenames):
    parallel = Parallel(n_jobs=-1, return_as="generator_unordered")
    segments = parallel(delayed(process_segments)(f) for f in filenames)

    # just consume segments so that tqdm shows progress
    for _ in tqdm(segments, total=len(filenames)):
        pass

def main_serial(filenames):
    for filename in tqdm(filenames):
        process_segments(filename)


filenames = data.loc[:200, "filename"]

print("joblib:", timeit.timeit(lambda: main_parallel(filenames), number=1))
print("serial:", timeit.timeit(lambda: main_serial(filenames), number=1))

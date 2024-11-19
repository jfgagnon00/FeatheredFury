import asyncio
import pandas
import timeit

from librosa import (
    load,
    power_to_db,
    resample,
    to_mono
)
from librosa.feature import melspectrogram
from numpy import (
    max as np_max,
    pad,
    save
)
from pandas import (
    Categorical,
    DataFrame,
)
from pathlib import Path
from ffury.configs import (
    load_config,
    ProjectConfig,
    PreprocessConfig
)

_MELSPECTROGRAM = "melspectrogram"
_SPECIE = "specie"
_SPECIES_CSV = "data_species.csv"
_PRIMARY_LABEL = "primary_label"
_COMMON_NAME = "common_name"
_FILENAME = "filename"
_LATITUDE = "latitude"
_LONGITUDE = "longitude"

project_config = load_config("/Users/jfgagnon/Projects/FeatheredFury/ffury.yaml")
config = project_config.preprocess
data = pandas.read_csv("/Users/jfgagnon/Projects/FeatheredFury/data/data_explored.csv")

def produce_segments(input_filename: str) -> list:
    input_filename = Path(input_filename)
    relative_prefix = Path.joinpath(Path(_MELSPECTROGRAM),
                                    input_filename.parents[0])
    spectrogram_prefix = Path.joinpath(project_config.paths.DATA_DIR,
                                        relative_prefix)
    spectrogram_prefix.mkdir(exist_ok=True, parents=True)

    audio_filename = project_config.get_audio_filename(input_filename)
    audio, sampling_rate = load(audio_filename)

    if len(audio) > 1:
        audio = to_mono(audio)

    if sampling_rate != config.clip_sampling_rate_hz:
        audio = resample(audio,
                            orig_sr=sampling_rate,
                            target_sr=config.clip_sampling_rate_hz)
        
    segment_length = config.segment_length
    segment_hop = config.segment_hop_length

    spectrograms = []

    for i, offset in enumerate(range(0, len(audio), segment_hop)):
        # extraire segment
        segment = audio[offset:offset + segment_length]

        # padding sur le dernier segment
        padding = segment_length - len(segment)
        if padding > 0:
            segment = pad(segment, (0, padding), mode="wrap")

        # log mel spectrogram
        S = melspectrogram(y=segment,
                            sr=config.clip_sampling_rate_hz,
                            n_fft=config.spectrogram_n_ftt,
                            hop_length=config.spectrogram_hop_length,
                            n_mels=config.spectrogram_n_mels,
                            fmin=config.spectrogram_fmin,
                            fmax=config.spectrogram_fmax)

        S_db = power_to_db(S,
                           ref=np_max)

        # sauvegarder spectrograms
        filename = f"{input_filename.stem}-{i:04d}.npy"
        save(spectrogram_prefix.joinpath(filename), S_db)

        # ajouter aux resultats
        spectrograms.append(relative_prefix.joinpath(filename))

    return spectrograms

async def async_produce_segments(input_filename: str) -> list:
    return produce_segments(input_filename)

async def async_main():
    await asyncio.gather(
        *[asyncio.to_thread(produce_segments, f) for f in data.loc[:20, "filename"]],
    )

def main_parallel():
    asyncio.run(async_main())

def main_plain():
    for f in data.loc[:20, "filename"]:
        produce_segments(f)

print( timeit.timeit(main_parallel, number=1) )
print( timeit.timeit(main_plain, number=1) )

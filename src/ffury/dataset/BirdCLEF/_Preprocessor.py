from librosa import (
    load,
    power_to_db,
    resample,
    to_mono
)
from librosa.feature import melspectrogram
from logging import Logger
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
from ...configs import (
    ProjectConfig,
    PreprocessConfig
)
from ...misc.concurrent import parallel_for
from ...misc.MetaObject import MetaObject

_MELSPECTROGRAM = "melspectrogram"
_SPECIE = "specie"
_SPECIES_CSV = "data_species.csv"
_PRIMARY_LABEL = "primary_label"
_COMMON_NAME = "common_name"
_FILENAME = "filename"
_LATITUDE = "latitude"
_LONGITUDE = "longitude"

class Preprocessor:
    def __init__(self,
                 project_config: ProjectConfig) -> None:
        self._project_config = project_config
        pass

    @property
    def _config(self) -> PreprocessConfig:
        return self._project_config.preprocess

    def produce_segments(self,
                         input_filename: str) -> list:
        input_filename = Path(input_filename)
        relative_prefix = Path.joinpath(Path(_MELSPECTROGRAM),
                                        input_filename.parents[0])
        spectrogram_prefix = Path.joinpath(self._project_config.paths.DATA_DIR,
                                           relative_prefix)
        spectrogram_prefix.mkdir(exist_ok=True, parents=True)

        audio_filename = self._project_config.get_audio_filename(input_filename)
        audio, sampling_rate = load(audio_filename)

        if len(audio) > 1:
            audio = to_mono(audio)

        if sampling_rate != self._config.clip_sampling_rate_hz:
            audio = resample(audio,
                             orig_sr=sampling_rate,
                             target_sr=self._config.clip_sampling_rate_hz)
            
        segment_length = self._config.segment_length
        segment_hop = self._config.segment_hop_length

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
                               sr=self._config.clip_sampling_rate_hz,
                               n_fft=self._config.spectrogram_n_ftt,
                               hop_length=self._config.spectrogram_hop_length,
                               n_mels=self._config.spectrogram_n_mels,
                               fmin=self._config.spectrogram_fmin,
                               fmax=self._config.spectrogram_fmax)

            # S_db = power_to_db(S,
            #                    ref=np_max)

            # # sauvegarder spectrograms
            # filename = f"{input_filename.stem}-{i:04d}.npy"
            # save(spectrogram_prefix.joinpath(filename), S_db)

            # # ajouter aux resultats
            # spectrograms.append(relative_prefix.joinpath(filename))

        return spectrograms

    # def run(self,
    #         output_filename: str,
    #         data: DataFrame) -> None:
    #     # create empty file
    #     dataframe = DataFrame(columns=[_MELSPECTROGRAM, _LATITUDE, _LONGITUDE, _SPECIE])
    #     dataframe.to_csv(output_filename, index=False)

    #     count = data.shape[0]

    #     with tqdm(total=count) as progress:
    #         # c'est pas bon; faut 1 seul encoding
    #         # le split non plus n'est pas bon -> on peut pas splitter par fichier
    #         # faut splitter sur les segments pour avoir qqch de balance dans le temps
    #         # genre le temps par espece...
    #         # ceci dit, c'est pas clair qu'un clip plus long a plus d'instance de chant
    #         species_future = self._executor.submit(self._produce_species,
    #                                                data)

    #         parallel_for(range(count),
    #                      self._produce_segments,
    #                      output_filename,
    #                      species_future,
    #                      data,
    #                      task_completed=lambda r: progress.update(1),
    #                      executor=self._executor)

    # def _produce_species(self,
    #                      input_filename: Path) -> MetaObject:
    #     # regrouper primary_label et common_name a partir du dataframe
    #     # les 2 proprietes sont uniques; represente espece
    #     species_str = data[[_PRIMARY_LABEL, _COMMON_NAME]].groupby(_PRIMARY_LABEL).first()
    #     species_str.reset_index(inplace=True)

    #     # transformer information d'espece en index (plus compacte sur disque)
    #     # one hot encoding pourra etre facilement reconstruit a partir de cet index
    #     species_codes = Categorical(data[_PRIMARY_LABEL],
    #                                 categories=species_str[_PRIMARY_LABEL])

    #     # validation
    #     assert data.shape[0] == species_codes.shape[0]

    #     filename = Path.joinpath(self._project_config.paths.DATA_DIR, _SPECIES_CSV)
    #     species_str.to_csv(filename, index=False)

    #     return MetaObject.from_kwargs(codes=species_codes.codes)

    # def _produce_segments(self,
    #                       output_filename: str,
    #                       species_future: Future,
    #                       data: DataFrame,
    #                       data_index: int) -> None:
    #     row = data.iloc[data_index]


    #     input_filename = row[_FILENAME]
        
    #     input_filename = Path(input_filename)
    #     relative_prefix = Path.joinpath(Path(_MELSPECTROGRAM),
    #                                     input_filename.parents[0])
    #     spectrogram_prefix = Path.joinpath(self._project_config.paths.DATA_DIR,
    #                                        Path(_MELSPECTROGRAM),
    #                                        input_filename.parents[0])
    #     spectrogram_prefix.mkdir(exist_ok=True, parents=True)

    #     audio_filename = self._project_config.get_audio_filename(input_filename)
    #     audio, sampling_rate = load(audio_filename)

    #     if len(audio) > 1:
    #         audio = to_mono(audio)

    #     if sampling_rate != self._config.clip_sampling_rate_hz:
    #         audio = resample(audio,
    #                          orig_sr=sampling_rate,
    #                          target_sr=self._config.clip_sampling_rate_hz)
            
    #     segment_length = self._config.segment_length
    #     segment_hop = self._config.segment_hop_length

    #     spectrograms = []

    #     for i, offset in enumerate(range(0, len(audio), segment_hop)):
    #         # extraire segment
    #         segment = audio[offset:offset + segment_length]

    #         # padding sur le dernier segment
    #         padding = segment_length - len(segment)
    #         if padding > 0:
    #             segment = pad(segment, (0, padding), mode="wrap")

    #         # log mel spectrogram
    #         S = melspectrogram(y=segment,
    #                            sr=self._config.clip_sampling_rate_hz,
    #                            n_fft=self._config.spectrogram_n_ftt,
    #                            hop_length=self._config.spectrogram_hop_length,
    #                            n_mels=self._config.spectrogram_n_mels,
    #                            fmin=self._config.spectrogram_fmin,
    #                            fmax=self._config.spectrogram_fmax)

    #         S_db = power_to_db(S,
    #                            ref=np_max)

    #         # sauvegarder spectrograms
    #         filename = f"{input_filename.stem}-{i:04d}.npy"
    #         save(spectrogram_prefix.joinpath(filename), S_db)

    #         # ajouter aux resultats
    #         spectrograms.append(relative_prefix.joinpath(filename))
            
    #     latitude = [row[_LATITUDE]] * len(spectrograms)
    #     longitude = [row[_LONGITUDE]] * len(spectrograms)

    #     species_codes = species_future.result().codes

    #     specie = [species_codes[data_index]] * len(spectrograms)

    #     dataframe = DataFrame({
    #         _MELSPECTROGRAM: spectrograms,
    #         _LATITUDE: latitude,
    #         _LONGITUDE: longitude,
    #         _SPECIE: specie
    #     })

    #     dataframe.to_csv(output_filename, 
    #                      mode="a+", 
    #                      index=False, 
    #                      header=False)

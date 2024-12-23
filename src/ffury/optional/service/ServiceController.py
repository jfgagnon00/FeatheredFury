import matplotlib

# permet d'exporter les figures en png
# sans etre sur le main thread
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from base64 import b64encode
from ffury.configs import (
    DatasetType,
    ProjectConfig
)
from ffury.transforms import (
    waveform_apply_config,
    waveform_from_file,
    spectrogram_from_audio
)
from io import BytesIO
from librosa import get_duration
from librosa.display import (
    specshow,
    waveshow
)
from numpy.typing import NDArray
from pandas import read_csv
from pathlib import Path
from typing import Tuple


class ServiceController:
    def __init__(self, project_config: ProjectConfig):
        self._config = project_config.preprocess
        self._init_species_label(project_config)
        self._load_model(project_config)

    @property
    def status(self) -> dict:
        return dict(controller="Created",
                    model="Not loaded" if self._model is None else "Loaded",
                    labels=self._species_label.copy())

    def predict(self, filename: str) -> None:
        audio, sampling_rate, spectrogram = self._transform(filename)
        duration = get_duration(y=audio, sr=sampling_rate)

        # transformer en groupe

        if not self._model is None:
            # prediction
            pass

        return self._render_waveform(audio, sampling_rate, duration, figsize=(10, 2)), \
               self._render_spectrogram(spectrogram, sampling_rate, duration, figsize=(10, 3))
    
    def _transform(self, filename: str) -> Tuple[NDArray, int, NDArray]:
        audio, sampling_rate = waveform_from_file(filename, 
                                                  self._config)
        
        audio, sampling_rate =  waveform_apply_config(audio, 
                                                      sampling_rate, 
                                                      self._config) 
        
        spectrogram = spectrogram_from_audio(audio, 
                                             sampling_rate,
                                             self._config)
        
        return audio, sampling_rate, spectrogram

    def _render_waveform(self,
                         audio: NDArray, 
                         sr: int, 
                         duration: float,
                         figsize: Tuple[int, int] =(10, 4),
                         format: str = "png") -> str:
        fig, ax = plt.subplots(figsize=figsize)
        waveshow(audio,
                 sr=sr,
                 ax=ax,
                 color="black")
        ax.set_xlim(left=0.0, right=duration)
        plt.xlabel("")
        plt.ylabel("Amplitude")
        plt.tight_layout()

        buffer_b64 = self._figure_to_b64(fig, format=format)
        plt.close(fig)

        return buffer_b64

    def _render_spectrogram(self,
                            spectrogram: NDArray, 
                            sr: int, 
                            duration: float,
                            figsize: Tuple[int, int] =(10, 4),
                            format: str = "png") -> str:
        fig, ax = plt.subplots(figsize=figsize)
        specshow(spectrogram,
                 x_axis='time',
                 y_axis='mel',
                 sr=sr,
                 ax=ax,
                 n_fft=self._config.spectrogram_n_ftt,
                 hop_length=self._config.spectrogram_hop_length,
                 cmap="gray_r")
        ax.set_xlim(left=0.0, right=duration)
        plt.xlabel("")
        plt.ylabel("Hz")
        plt.tight_layout()

        buffer_b64 = self._figure_to_b64(fig, format=format)
        plt.close(fig)

        return buffer_b64

    def _figure_to_b64(self, figure, format) -> str:
        buffer = BytesIO()
        figure.savefig(buffer, format=format)
        buffer.seek(0)

        buffer_b64 = b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()

        return buffer_b64

    def _load_model(self, project_config: ProjectConfig) -> None:
        self._model  = None
        filename = Path.joinpath(project_config.paths.MODELS_DIR, "Model.keras")
        if Path.is_file(filename):
            from keras.models import load_model
            self._model = load_model(filename)

    def _init_species_label(self, project_config: ProjectConfig) -> None:
        filename = project_config.get_csv_filename(DatasetType._SPECIES)
        species_df = read_csv(filename)
        self._species_label = species_df["common_name"].to_list()

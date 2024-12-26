import matplotlib

# permet d'exporter les figures en png
# sans etre sur le main thread
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from base64 import b64encode
from flask import current_app
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
        if self._model is None:
            # ne peut pas faire d'inference sans modele
            return None, None, None

        audio, sampling_rate, spectrogram = self._transform(filename)
        group_batches = self._make_groups(spectrogram)

        if group_batches is None:
            # ne peut pas faire d'inference sans donnees
            return None, None, None

        duration = get_duration(y=audio, sr=sampling_rate)
        predictions = self._make_prediction(group_batches)

        logger = current_app.config["LOGGER"]
        logger.info(f"Duree audio: {round(duration * 1000, 1)} ms")
        logger.info(f"Duree groupe: {self._config.group_ms_infos()[0]} ms")
        logger.info(f"Spectrogramme shape: {spectrogram.shape}")
        logger.info(f"Groupe info: {self._config.group_segment_count} {self._config.group_frame_infos()}")
        logger.info(f"Groupe batch shape: {group_batches.shape}")
        logger.info(f"Num predictions: {len(predictions)}")

        return self._render_waveform(audio, sampling_rate, duration, figsize=(11, 1.5)), \
               self._render_spectrogram(spectrogram, sampling_rate, duration, figsize=(11, 2.9)), \
               predictions
    
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

    def _make_groups(self, 
                     spectrogram: NDArray) -> NDArray:
        # information pour slicer le spectrogram
        group_length, segment_length, group_hop_length = self._config.group_frame_infos()

        groups = []
        group_start = 0

        # les groupe se slice dans l'axe du temps - width ou axe 1 pour numpy
        group_count = spectrogram.shape[1] // group_length
        for _ in range(group_count):
            # slicer 1 groupe a la fois
            segments = []
            segment_start = group_start
            for _ in range(self._config.group_segment_count):
                segment = spectrogram[:, segment_start:segment_start + segment_length]
                segments.append(segment)
                segment_start += group_hop_length

            # self._config.group_segment_count segments consecutifs
            # pour keras, ca signifie channel last
            group = np.dstack(segments)
            groups.append(group)

            # passer au groupe suivant
            group_start += group_length

        if len(groups) > 0:
            # on concatene tous les groupes
            return np.stack(groups)

        # pas assez de donnee pour fair 1 groupe
        return None

    def _make_prediction(self,
                         batches: NDArray) -> list:
        species_prob = self._model.predict(batches, verbose=0)
        species_index = np.argmax(species_prob, axis=1)
        species_pred = species_prob[np.arange(species_prob.shape[0]), species_index] > 0.25

        logger = current_app.config["LOGGER"]
        logger.info(f"Prediction proba. shape: {species_prob.shape}")
        logger.info(f"Prediction index shape: {species_index.shape}")
        logger.info(f"Prediction shape: {species_pred.shape}")

        # TODO: la prediction pourrait faire mieux comme les segments se chevauchent
        #       pour le moment 1 prediction par groupe
        group_length, _, group_hop_length = self._config.group_ms_infos()
        predictions = []

        time = group_length // 2
        for i in range(species_prob.shape[0]):
            if species_pred[i]:
                specie_index = species_index[i]
                name = self._species_label[specie_index]
                label = self._species[specie_index]
                prediction = dict(
                    name=f"{name} [{label}]",
                    time=time,
                    probabilities=species_prob[i].tolist(),
                    info_url=f"https://ebird.org/species/{label}",
                )
                predictions.append(prediction)

            time += group_length

        return predictions

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
        self._species = species_df["primary_label"].to_list()

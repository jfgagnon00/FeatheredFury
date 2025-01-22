import json
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
from ffury.misc.logging import pretty_format
from ffury.optional.monitoring.misc.timestamp import timestamp_now
from ffury.optional.monitoring.azure_blob_storage import (
    upload,
    upload_file
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
from pandas import (
    DataFrame,
    read_csv
)
from pathlib import Path
from typing import (
    Dict,
    List,
    Tuple
)


from ..keras_adapters import _load_model


class ServiceController:
    def __init__(self, project_config: ProjectConfig):
        self._paths_config = project_config.paths
        self._preprocess_config = project_config.preprocess
        self._init_species_label(project_config)
        self._init_thresholds(project_config)
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
        predictions, features = self._make_prediction(group_batches)
        id = self._monitor(features, predictions)

        logger = current_app.config["LOGGER"]
        logger.info(f"Duree audio: {round(duration * 1000, 1)} ms")
        logger.info(f"Duree groupe: {self._preprocess_config.group_ms_infos()[0]} ms")
        logger.info(f"Spectrogramme shape: {spectrogram.shape}")
        logger.info(f"Groupe info: {self._preprocess_config.group_segment_count} {self._preprocess_config.group_frame_infos()}")
        logger.info(f"Groupe batch shape: {group_batches.shape}")
        logger.info(f"Num predictions: {len(predictions)}")

        return self._render_waveform(audio, sampling_rate, duration, figsize=(11, 1.5)), \
               self._render_spectrogram(spectrogram, sampling_rate, duration, figsize=(11, 2.9)), \
               predictions, \
               id
    
    def _transform(self, filename: str) -> Tuple[NDArray, int, NDArray]:
        audio, sampling_rate = waveform_from_file(filename, 
                                                  self._preprocess_config)
        
        audio, sampling_rate =  waveform_apply_config(audio, 
                                                      sampling_rate, 
                                                      self._preprocess_config) 
        
        spectrogram = spectrogram_from_audio(audio, 
                                             sampling_rate,
                                             self._preprocess_config)
        
        return audio, sampling_rate, spectrogram

    def _make_groups(self, 
                     spectrogram: NDArray) -> NDArray:
        # information pour slicer le spectrogram
        group_length, segment_length, group_hop_length = self._preprocess_config.group_frame_infos()

        groups = []
        group_start = 0

        # les groupe se slice dans l'axe du temps - width ou axe 1 pour numpy
        group_count = spectrogram.shape[1] // group_length
        for _ in range(group_count):
            # slicer 1 groupe a la fois
            segments = []
            segment_start = group_start
            for _ in range(self._preprocess_config.group_segment_count):
                segment = spectrogram[:, segment_start:segment_start + segment_length]
                segments.append(segment)
                segment_start += group_hop_length

            # self._preprocess_config.group_segment_count segments consecutifs
            group = np.stack(segments, axis=0)
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
        species_prob, species_features = self._model.predict(batches, verbose=0)
        species_index = np.argmax(species_prob, axis=1)
        species_pred = species_prob[np.arange(species_prob.shape[0]), species_index] > self._thresholds[species_index]

        logger = current_app.config["LOGGER"]

        logger.info(f"Features. shape: {species_features.shape}")
        logger.info(f"Prediction proba. shape: {species_prob.shape}")
        logger.info(f"Prediction proba.:")
        logger.info(np.round(species_prob, 4))
        logger.info(f"Prediction proba. sum:")
        logger.info(np.round(np.sum(species_prob, axis=1), 4) )

        logger.info(f"Prediction index shape: {species_index.shape}")
        logger.info("Prediction index:")
        logger.info(species_index)

        logger.info(f"Prediction shape: {species_pred.shape}")

        # TODO: la prediction pourrait faire mieux comme les segments se chevauchent
        #       pour le moment 1 prediction par groupe
        group_length, _, group_hop_length = self._preprocess_config.group_ms_infos()
        predictions = []

        time = group_length // 2
        for i in range(species_prob.shape[0]):
            if species_pred[i]:
                specie_index = species_index[i]
                name = self._species_label[specie_index]
                label = self._species[specie_index]
                prediction = dict(
                    name=f"{name} [{label}]",
                    label=int(specie_index),
                    time=time,
                    probabilities=species_prob[i].tolist(),
                    info_url=f"https://ebird.org/species/{label}",
                )
                predictions.append(prediction)

            time += group_length

        return predictions, species_features

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
                 n_fft=self._preprocess_config.spectrogram_n_ftt,
                 hop_length=self._preprocess_config.spectrogram_hop_length,
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
        self._model  = _load_model(project_config)

    def _init_species_label(self, project_config: ProjectConfig) -> None:
        filename = project_config.get_csv_filename(DatasetType._SPECIES)
        species_df = read_csv(filename)
        self._species_label = species_df["common_name"].to_list()
        self._species = species_df["primary_label"].to_list()

    def _init_thresholds(self, project_config: ProjectConfig) -> None:
        thresholds = project_config.service.predict_thresholds

        # si on utilise 1 float pour le thresholds, le repliquer pout toute les classes
        if not isinstance(thresholds, list):
            thresholds = [thresholds] * project_config.num_classes

        if len(thresholds) != project_config.num_classes:
            raise ValueError(f"Taille liste thresholds ne correspond pas aux nombre de classes: {len(self._thresholds)} vs {project_config.num_classes}")

        self._thresholds = np.array(thresholds)

    def _monitor(self, 
                 features: NDArray,
                 predictions: List[Dict]) -> str:
        if features is None or len(features.shape) != 3:
            return ""

        logger = current_app.config["LOGGER"]

        try:
            group_features = np.mean(features, axis=1)

            ts = timestamp_now()
            id = str(ts)
            id = id.replace(".", "-")
            id = id.replace(",", "-")
            id = "p" + id

            logger.info(f"Monitoring id        : {id}")
            logger.info(f"Features. shape      : {features.shape}")
            logger.info(f"Group Features. shape: {group_features.shape}")
            logger.info(f"Predictions          : {len(predictions)}")

            features_df = DataFrame(data=group_features,
                                    columns=[f"feat_{i}" for i in range(group_features.shape[-1])])
            filename = Path.joinpath(self._paths_config.BUILD_DIR, "prediction_features.csv")
            filename.parent.mkdir(parents=True, exist_ok=True)
            features_df.to_csv(filename, index=False)
            upload_file(str(filename), id, "features", ts)
            filename.unlink()

            predictions = json.dumps(predictions)
            upload(id, "predictions", predictions.encode(encoding="UTF-8"), ts)

            return id
        except Exception as e:
            logger.error("Erreur lors du monitoring")
            logger.error(str(e))
            return ""

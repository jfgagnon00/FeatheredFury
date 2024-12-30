from typing import (
    Any,
    Tuple
)

from ffury.configs import ProjectConfig
from ffury.misc.IFactory import IFactory
from ffury.yaml.yaml_decorators import YamlDeserializable

from .KerasLoss import keras_loss
from .KerasOptimizer import keras_optimizer


@YamlDeserializable
class KerasDummyModelFactory(IFactory):
    """
    Modele utlise pour tester le pipeline. Ne doit pas etre 
    utliser autrement.
    """
    def __init__(self):
        self.model_name = "Model" # "KerasDummyModelFactory"

    def create_from_config(self, project_config: ProjectConfig) -> Any:
        # (num_segments, n_mels, n_frames)
        input_shape = project_config.preprocess.train_input_shape()

        model = self._create_model(input_shape,
                                   project_config.num_classes)
        if len(self.model_name) > 0:
            model.name = self.model_name

        train_config = project_config.train
        train_parameters = train_config.parameters
        model.compile(optimizer=keras_optimizer(train_parameters), 
                      loss=keras_loss(train_parameters))

        model.summary()

        return model

    def _create_model(self, 
                      input_shape: Tuple[int, int, int],
                      num_classes: int) -> Any:
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from keras import Sequential
        from keras.layers import (
            BatchNormalization,
            Dense, 
            Dropout,
            Input, 
            GlobalMaxPooling1D,
            Reshape, 
            TimeDistributed, 
        )

        target_shape = (input_shape[0], input_shape[1] * input_shape[2])

        segment_net = Sequential([
            Dense(units=512, activation="relu"),
            # BatchNormalization(),
            # Dropout(rate=0.1),
            # Dense(units=128, activation="relu"),
            Dense(units=num_classes, activation="sigmoid")
        ])

        return Sequential([
            Input(shape=input_shape),
            Reshape(target_shape=target_shape),
            TimeDistributed(segment_net),
            GlobalMaxPooling1D()
        ])

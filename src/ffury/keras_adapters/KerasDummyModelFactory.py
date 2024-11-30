from math import prod
from typing import (
    Any,
    Tuple
)

from .KerasLoss import keras_loss
from .KerasOptimizer import keras_optimizer

from ..configs import ProjectConfig
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasDummyModelFactory:
    def __init__(self) -> None:
        self._name = "KerasDummyModelFactory"

    def create_from_config(self, project_config: ProjectConfig) -> None:
        input_shape = project_config.preprocess.train_input_shape()

        model = self._create_model(input_shape)
        if len(self._name) > 0:
            model.name = self._name

        model.compile(optimizer=keras_optimizer(project_config.train.parameters), 
                      loss=keras_loss(project_config.train.parameters), 
                      metrics=["accuracy"])

        model.summary()

        return model

    def _create_model(self, input_shape: Tuple[int, int, int]) -> Any:
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from keras import Sequential
        from keras.layers import Dense, Flatten, Input

        return Sequential([
            Input(shape=input_shape),
            Flatten(),
            Dense(prod(input_shape), activation="sigmoid")
        ])

from typing import (
    Any,
    Tuple
)

from .KerasLoss import keras_loss
from .KerasOptimizer import keras_optimizer

from ..configs import ProjectConfig
from ..misc.IFactory import IFactory
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasDummyModelFactory(IFactory):
    def __init__(self):
        self.name = "KerasDummyModelFactory"
        self.num_classes = 0

    def create_from_config(self, project_config: ProjectConfig) -> Any:
        input_shape = project_config.preprocess.train_input_shape()

        model = self._create_model(input_shape)
        if len(self.name) > 0:
            model.name = self.name

        train_config = project_config.train
        train_parameters = train_config.parameters
        model.compile(optimizer=keras_optimizer(train_parameters), 
                      loss=keras_loss(train_parameters))

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
            Dense(self.num_classes, activation="sigmoid")
        ])

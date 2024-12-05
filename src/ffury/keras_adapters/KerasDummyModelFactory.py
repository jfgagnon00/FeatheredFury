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
    """
    Modele utlise pour tester le pipeline. Ne doit pas etre 
    utliser autrement.
    """
    def __init__(self):
        self.model_name = "KerasDummyModel"

    def create_from_config(self, project_config: ProjectConfig) -> Any:
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
        from keras.layers import Dense, Flatten, Input

        return Sequential([
            Input(shape=input_shape),
            Flatten(),
            Dense(num_classes, activation="sigmoid")
        ])

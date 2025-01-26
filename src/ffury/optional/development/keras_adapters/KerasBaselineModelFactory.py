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
class KerasBaselineModelFactory(IFactory):
    """
    Modele utlise pour tester le pipeline.
    """
    def __init__(self):
        self.model_name = "Model"

    def create_from_config(self, project_config: ProjectConfig) -> Any:
        # (num_segments, n_mels, n_frames)
        input_shape = project_config.preprocess.train_input_shape()

        group_model, segment_model = self._create_model(input_shape,
                                                        project_config.num_classes)
        if len(self.model_name) > 0:
            group_model.name = self.model_name

        train_config = project_config.train
        train_parameters = train_config.parameters
        group_model.compile(optimizer=keras_optimizer(train_parameters), 
                            loss=keras_loss(train_parameters))

        print()
        group_model.summary()

        print()
        segment_model.summary()

        return group_model

    def _create_model(self, 
                      input_shape: Tuple[int, int, int],
                      num_classes: int) -> Any:
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from keras.models import Model
        from keras.layers import (
            Dense, 
            Input, 
            GlobalMaxPooling1D,
            Reshape, 
            TimeDistributed, 
        )

        # les attentes du pipleine est que le model ait comme output
        # les predictions mais aussi ses features, on doit donc utiliser 
        # l'api functionnelle de Keras et non Sequential

        segment_features = input_shape[1] * input_shape[2]

        from ffury.optional.keras_adapters._KerasBaselineSegmentFeatures import _KerasBaselineSegmentFeatures
        segment_model = _KerasBaselineSegmentFeatures(shape=(segment_features,),
                                                      name="SegmentFeatures")

        group_inputs        = Input(shape=input_shape)
        group_features      = Reshape(target_shape=(input_shape[0], segment_features))(group_inputs)
        group_features      = TimeDistributed(segment_model,
                                              name="GroupFeatures")(group_features)
        group_probabilities = Dense(units=num_classes, 
                                    activation="sigmoid",
                                    name="GroupProbabilities")(group_features)
        group_voting        = GlobalMaxPooling1D(name="GroupVoting")(group_probabilities)
        group_model         = Model(inputs=group_inputs, 
                                    outputs=[group_voting, 
                                            group_features])

        return group_model, segment_model

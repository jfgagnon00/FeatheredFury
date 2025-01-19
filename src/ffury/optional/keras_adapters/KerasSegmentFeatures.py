from keras.models import Model
from keras.layers import (
    BatchNormalization,
    Dense, 
    Dropout,
    Input
)


class KerasSegmentFeatures(Model):
    def __init__(self, shape=None, **kwargs):
        super().__init__()

        if not shape is None:
            segment_inputs   = Input(shape=shape)
            segment_features = BatchNormalization()(segment_inputs)
            segment_features = Dropout(rate=0.2)(segment_features)
            segment_features = Dense(units=512, activation="relu")(segment_features)

            segment_features = BatchNormalization()(segment_features)
            segment_features = Dropout(rate=0.2)(segment_features)
            segment_features = Dense(units=2048, activation="relu")(segment_features)

            self._shape = shape
            self._model = Model(inputs=segment_inputs, 
                                outputs=segment_features,
                                **kwargs)

    def call(self, inputs):
        return self._model(inputs)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self._model.layers[-1].units)
    
    def summary(self, **kwargs):
        self._model.summary(**kwargs)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "internal_shape": self._shape,
            "internal_model": self._model.get_config()
        })
        return config

    @classmethod
    def from_config(cls, config):
        instance = KerasSegmentFeatures()
        instance._shape = config["internal_shape"]
        instance._model = Model.from_config(config["internal_model"])
        return instance

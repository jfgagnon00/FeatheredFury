from keras.models import Model
from keras.layers import (
    BatchNormalization,
    Conv2D,
    Dropout,
    Flatten,
    Input,
    MaxPooling2D,
)


class _KerasCNNSegmentFeatures(Model):
    def __init__(self, shape=None, **kwargs):
        super().__init__()

        if not shape is None:
            segment_inputs   = Input(shape=shape)

            # Conv block #1
            segment_features = BatchNormalization()(segment_inputs)
            segment_features = Conv2D(filters=32, 
                                      kernel_size=(5, 5),
                                      padding="same",
                                      data_format="channels_last",
                                      activation="relu")(segment_features)
            segment_features = MaxPooling2D(pool_size=(4, 2))(segment_features)
            segment_features = Dropout(rate=0.2)(segment_features)

            # Conv block #2
            segment_features = Conv2D(filters=64, 
                                      kernel_size=(5, 5),
                                      padding="same",
                                      data_format="channels_last",
                                      activation="relu")(segment_features)
            segment_features = MaxPooling2D(pool_size=(4, 2))(segment_features)
            segment_features = Dropout(rate=0.2)(segment_features)

            # Conv block #3
            segment_features = Conv2D(filters=96, 
                                      kernel_size=(5, 5),
                                      padding="same",
                                      data_format="channels_last",
                                      activation="relu")(segment_features)
            segment_features = Flatten()(segment_features)

            self._model = Model(inputs=segment_inputs, 
                                outputs=segment_features,
                                **kwargs)

    def call(self, inputs):
        return self._model(inputs)

    def compute_output_shape(self, input_shape):
        current_shape = input_shape
        for l in self._model.layers[1:]:
            current_shape = l.compute_output_shape(current_shape)
        return current_shape

    def summary(self, **kwargs):
        self._model.summary(**kwargs)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "internal_model_config": self._model.get_config()
        })
        return config

    @classmethod
    def from_config(cls, config):
        instance = cls()
        instance._model = Model.from_config(config["internal_model_config"])
        return instance

from keras.callbacks import Callback
from typing import Callable


class KerasMetricCallback(Callback):
    def __init__(self, 
                 x_train, y_train,
                 x_validation, y_validation,
                 metrics: Callable):
        self._x_train = x_train
        self._y_train_true = y_train
        self._x_validation = x_validation
        self._y_validation_true = y_validation
        self._metrics = metrics

    def on_epoch_end(self, epoch, logs=None):
        y_pred = self.model.predict(self._x_train)
        metrics_train = self._metrics(self._y_train_true,
                                      y_pred)

        y_pred = self.model.predict(self._x_validation)
        metrics_validation = self._metrics(self._y_validation_true,
                                           y_pred)

        print(metrics_train)
        print(metrics_validation)

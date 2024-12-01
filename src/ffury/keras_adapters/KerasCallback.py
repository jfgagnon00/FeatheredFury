from keras.callbacks import Callback
from typing import (
    Any,
    Callable,
    List
)

from ..misc.logging import (
    create_logger,
    pretty_format
)


class KerasCallback(Callback):
    """
    Collige les metriques et les log via Neptune AI
    """
    def __init__(self,
                 class_labels: List[str],
                 x_train: Any, 
                 y_train: Any,
                 x_validation: Any, 
                 y_validation: Any,
                 metrics: Callable):
        self._class_labels = class_labels
        self._x_train = x_train
        self._y_train_true = y_train
        self._x_validation = x_validation
        self._y_validation_true = y_validation
        self._metrics = metrics
        self._logger = create_logger(file=__file__)

    def on_epoch_end(self, epoch, logs=None):
        y_pred = self.model.predict(self._x_train, verbose=0)
        metrics_train = self._metrics(self._class_labels,
                                      self._y_train_true,
                                      y_pred,)

        y_pred = self.model.predict(self._x_validation, verbose=0)
        metrics_validation = self._metrics(self._class_labels,
                                           self._y_validation_true,
                                           y_pred)

        if False:
            if not logs is None:
                self._logger.info("Logs")
                self._logger.info( pretty_format(logs) )

            self._logger.info("metrics_train")
            self._logger.info( pretty_format(metrics_train) )

            self._logger.info("metrics_validation")
            self._logger.info( pretty_format(metrics_validation) )
            self._logger.info("")
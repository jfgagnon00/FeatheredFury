from keras.callbacks import Callback
from typing import (
    Any,
    List
)

from ..misc.IMeasurable import IMeasurable
from ..neptune import NeptuneRun

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
                 run: NeptuneRun,
                 measurable: IMeasurable):
        self._class_labels = class_labels
        self._x_train = x_train
        self._y_train_true = y_train
        self._x_validation = x_validation
        self._y_validation_true = y_validation
        self._run = run
        self._measurable = measurable

    def on_epoch_end(self, epoch, logs=None):
        y_pred = self.model.predict(self._x_train, verbose=0)
        measure_train = self._measurable(self._class_labels,
                                         self._y_train_true,
                                         y_pred)

        y_pred = self.model.predict(self._x_validation, verbose=0)
        measure_validation = self._measurable(self._class_labels,
                                              self._y_validation_true,
                                              y_pred,
                                              "val")

        if not logs is None:
            measure_train["loss"] = logs["loss"]
            measure_validation["val_loss"] = logs["val_loss"]

        self._run.append_measures(epoch, measure_train)
        self._run.append_measures(epoch, measure_validation)

from copy import deepcopy
from keras.callbacks import Callback
from keras.models import (
    load_model,
    save_model
)
from typing import (
    Any,
    List
)

from ffury.misc.IMeasurable import IMeasurable
from ffury.misc.logging import create_logger

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
                 measurable: IMeasurable,
                 model_checkpoint: str):
        self._class_labels = class_labels
        self._x_train = x_train
        self._y_train_true = y_train
        self._x_validation = x_validation
        self._y_validation_true = y_validation
        self._run = run
        self._measurable = measurable
        self._model_checkpoint_pattern = model_checkpoint
        self._best_model_checkpoint = None
        self._best_measure_checkpoint = None
        self._best_epoch = None
        self._logger = create_logger(file=__file__)

    @property
    def best_model(self) -> Any:
        return self._best_model

    @property
    def best_model_checkpoint(self) -> str:
        return self._best_model_checkpoint

    @property
    def best_measure_name(self) -> str:
        return self._best_measure_checkpoint[0]

    @property
    def best_measure_value(self) -> str:
        return self._best_measure_checkpoint[1]

    @property
    def best_epoch(self) -> str:
        return self._best_epoch
    
    def on_epoch_end(self, epoch, logs=None):
        # le modele a 2 outputs :  prediction + features (pour le monitoring)
        y_pred, _ = self.model.predict(self._x_train, verbose=0)
        measure_train = self._measurable(self._class_labels,
                                         self._y_train_true,
                                         y_pred)

        y_pred, _ = self.model.predict(self._x_validation, verbose=0)
        measure_validation = self._measurable(self._class_labels,
                                              self._y_validation_true,
                                              y_pred,
                                              "val")

        if not logs is None:
            measure_train["loss"] = logs["loss"]
            measure_validation["val_loss"] = logs["val_loss"]

        self._run.append_measures(epoch, measure_train)
        self._run.append_measures(epoch, measure_validation)

        measure_checkpoint = self._measurable.check_point_measurable(measure_validation,
                                                                     "val")
        if self._best_measure_checkpoint is None or \
           measure_checkpoint[1] > self._best_measure_checkpoint[1]:
            self._best_epoch = epoch
            self._best_measure_checkpoint = deepcopy(measure_checkpoint)
            self._best_model_checkpoint = self._model_checkpoint_pattern.format(epoch=epoch)
            save_model(self.model, self._best_model_checkpoint)
            self._logger.info(f"\nNouveau meilleur modele:\n  {self._best_model_checkpoint}, {measure_checkpoint}")

    def log_test_and_thresholds(self,
                                epoch: int,
                                x_test: Any, 
                                y_test: Any,
                                thresholds_optimization_steps: float) -> None:
        if self._best_model_checkpoint is None:
            return

        model = load_model(self._best_model_checkpoint)
        y_pred, _ = model.predict(x_test, verbose=0)
        measure_test = self._measurable(self._class_labels,
                                        y_test,
                                        y_pred,
                                        "test")
        self._run.append_measures(epoch, measure_test)

        y_pred, _ = model.predict(self._x_validation, verbose=0)
        thresholds = self._measurable.optimize_thesholds(self._y_validation_true, 
                                                         y_pred,
                                                         thresholds_optimization_steps)
        self._run.log_model_thresholds(thresholds)
        self._logger.info(f"Thresholds optimises: {thresholds}")

import numpy as np


from copy import deepcopy
from sklearn.metrics import (
    precision_recall_curve,
    classification_report
)
from numpy.typing import NDArray
from typing import (
    Any,
    List,
    Tuple,
    Union
)

from ffury.optional.keras_adapters import _predict_from_probabilities
from ffury.misc.IMeasurable import IMeasurable
from ffury.yaml.yaml_decorators import YamlDeserializable

_F1_KEY = "f1"
_F1_SCORE_KEY = "f1-score"
_PRECISION_KEY = "precision"
_RECALL_KEY = "recall"


@YamlDeserializable
class KerasMeasurable(IMeasurable):
    def __init__(self) -> None:
        self.average = "macro"
        self._class_labels = None

    def __call__(self, 
                 y_true: NDArray, 
                 y_pred: NDArray,
                  y_pred_thresholds: Union[float, NDArray] = 0.5,
                 measure_prefix: str = None) -> Any:
        # calculer les metriques
        report = classification_report(_predict_from_probabilities(y_true=y_true), 
                                       _predict_from_probabilities(y_pred=y_pred, thresholds=y_pred_thresholds),
                                       target_names=self._class_labels,
                                       output_dict=True,
                                       zero_division=0.0)

        measure_prefix = KerasMeasurable._measure_prefix(measure_prefix)

        new_report = {}

        # report est liste par label
        # le transformer pour le lister par metrique
        for label in (self._class_labels + [self._average_key()]):
            for metric, metric_name in ((_F1_SCORE_KEY, _F1_KEY),
                                        (_PRECISION_KEY, _PRECISION_KEY),
                                        (_RECALL_KEY, _RECALL_KEY)):
                new_report[f"{measure_prefix}{metric_name}/{label}"] = report[label][metric]

        return new_report
    
    def check_point_measurable(self, 
                               measure: Any,
                               measure_prefix: str = None) -> Tuple[str, float]:
        measure_prefix = KerasMeasurable._measure_prefix(measure_prefix)
        key = f"{measure_prefix}{_F1_KEY}/{self._average_key()}"
        return key, measure[key]

    def init_class_labels(self, 
                          class_labels: List[str]) -> None:
        self._class_labels = deepcopy(class_labels)
        self._class_labels.append("unknown")

    def optimize_thesholds(self,
                           y_true: NDArray, 
                           y_pred: NDArray) -> List[float]:
        best_thresholds = []
        for c in range(y_true.shape[-1]):
            precision, recall, thresholds = precision_recall_curve(y_true[:, c], y_pred[:, c])
            f1_scores = (2 * precision * recall) / (precision + recall)
            best_f1_score_index = np.argmax(f1_scores)
            best_thresholds.append( round(thresholds[best_f1_score_index], 5) )
        return best_thresholds

    def _average_key(self) -> str:
        return f"{self.average} avg"

    @staticmethod
    def _measure_prefix(measure_prefix: str) -> str:
        return "" if measure_prefix is None else f"{measure_prefix}_"

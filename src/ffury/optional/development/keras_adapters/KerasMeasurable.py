from numpy import argmax
from sklearn.metrics import (
    average_precision_score,
    classification_report
)
from typing import (
    Any,
    List,
    Tuple
)

from ffury.misc.IMeasurable import IMeasurable
from ffury.yaml.yaml_decorators import YamlDeserializable

_AVERAGE_PRECISION_KEY = "ap"
_F1_KEY = "f1"
_F1_SCORE_KEY = "f1-score"
_PRECISION_KEY = "precision"
_RECALL_KEY = "recall"


@YamlDeserializable
class KerasMeasurable(IMeasurable):
    def __init__(self) -> None:
        self.average = "macro"

    def __call__(self, 
                 class_labels: List[str], 
                 y_true: Any, 
                 y_pred: Any,
                 measure_prefix: str = None) -> Any:
        # calculer les metriques
        ap = average_precision_score(y_true, 
                                     y_pred, 
                                     average=self.average)
        report = classification_report(argmax(y_true, axis=-1), 
                                       argmax(y_pred, axis=-1),
                                       target_names=class_labels,
                                       output_dict=True,
                                       zero_division=0.0)

        measure_prefix = KerasMeasurable._measure_prefix(measure_prefix)

        new_report = {}
        new_report[f"{measure_prefix}{_AVERAGE_PRECISION_KEY}/{self._average_key()}"] = ap

        # report est liste par label
        # le transformer pour le lister par metrique
        for label in (class_labels + [self._average_key()]):
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

    def _average_key(self) -> str:
        return f"{self.average} avg"

    @staticmethod
    def _measure_prefix(measure_prefix: str) -> str:
        return "" if measure_prefix is None else f"{measure_prefix}_"

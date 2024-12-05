from abc import ABC, abstractmethod
from typing import (
    Any,
    List,
    Tuple
)


class IMeasurable(ABC):
    """
    Interface pour toutes les metriques
    """

    @abstractmethod
    def __call__(self,
                 class_labels: List[str],
                 y_true: Any,
                 y_pred: Any,
                 measure_prefix: str = None) -> Any:
        """
        Classes concretes doivent implementer cette methode 
        pour calculer et retourner les metriques
        """
        pass

    @abstractmethod
    def check_point_measurable(self, 
                               measure: Any,
                               measure_prefix: str = None) -> Tuple[str, float]:
        """
        Classes concretes doivent implementer cette methode 
        pour obtenir le nom de la metrique et sa valeur pour comparer les checkpoint
        """
        pass
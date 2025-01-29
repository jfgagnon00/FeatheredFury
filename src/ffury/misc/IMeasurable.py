from abc import ABC, abstractmethod
from numpy.typing import NDArray
from typing import (
    Any,
    List,
    Tuple,
    Union,
)


class IMeasurable(ABC):
    """
    Interface pour toutes les metriques
    """

    @abstractmethod
    def __call__(self,
                 y_true: NDArray,
                 y_pred: NDArray,
                 y_pred_thresholds: Union[float, NDArray] = 0.5,
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

    @abstractmethod
    def init_class_labels(self,
                          class_labels: List[str]) -> None:
        """
        Classes concretes doivent implementer cette methode 
        pour initialiser les labels des classes. La gestion de la classe
        "unknown" implicite est laisse aux implementations concretes.
        """
        pass

    @abstractmethod
    def optimize_thesholds(self,
                           y_true: NDArray, 
                           y_pred: NDArray) -> List[float]:
        """
        Classes concretes doivent implementer cette methode 
        pour obtenir les thresholds de classification optimaux
        """
        pass
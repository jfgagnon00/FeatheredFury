from abc import ABC, abstractmethod
from typing import (
    Any,
    List
)


class IMeasurable(ABC):
    """
    Interface pour toutes les metriques
    """

    @abstractmethod
    def __call__(self,
                 class_labels: List[str],
                 y_true: Any,
                 y_pred: Any) -> Any:
        """
        Classes concretes doivent implementer cette methode 
        pour calculer et retourner les metriques
        """
        pass
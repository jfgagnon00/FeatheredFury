from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    List
)

from ..configs import (
    PathsConfig,
    TrainParameters
)

class ITrainable(ABC):
    """
    Interface pour tous les trainer
    """

    @abstractmethod
    def __call__(self,
                 paths: PathsConfig,
                 parameters: TrainParameters,
                 metrics: Callable,
                 model: Any, 
                 class_labels: List[str],
                 x_train: Any,
                 y_train: Any,
                 x_valdation: Any,
                 y_valdation: Any) -> None:
        """
        Classes concretes doivent implementer cette methode 
        pour lancer entrainement
        """
        pass
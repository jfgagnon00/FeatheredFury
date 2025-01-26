from abc import ABC, abstractmethod
from typing import (
    Any,
    List
)

from ..configs import (
    PathsConfig,
    TrainParameters
)
from ..misc.IMeasurable import IMeasurable

class ITrainable(ABC):
    """
    Interface pour tous les trainer
    """

    @abstractmethod
    def __call__(self,
                 run, # NeptuneRun
                 paths: PathsConfig,
                 parameters: TrainParameters,
                 measurable: IMeasurable,
                 model: Any, 
                 class_labels: List[str],
                 x_train: Any,
                 y_train: Any,
                 x_valdation: Any,
                 y_valdation: Any,
                 x_test: Any,
                 y_test: Any) -> None:
        """
        Classes concretes doivent implementer cette methode 
        pour lancer entrainement
        """
        pass
from abc import ABC, abstractmethod
from typing import Any

from ..configs import ProjectConfig


class IFactory(ABC):
    """
    Interface pour tous les factory
    """

    @abstractmethod
    def create_from_config(self, project_config: ProjectConfig) -> Any:
        """
        Classe concrete doivent implementer cette methode pour creer leur
        objet a partir des configuration du projet
        """
        pass
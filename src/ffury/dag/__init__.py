"""
Encapsule toutes les taches reliees au DAG pour l'entrainement
d'un modele.

Notes
Le preprocessing est un cas particulier. Les donnees initiales
doivent etre manipuler afin d'obtenir des groupes/segments. Cette
transformation est couteuse et change les distributions des 
ensembles train/test/validation. Il a donc ete decide qu'elle 
serait fait 1x au preprocessing. Changer ses parametres demande
une nouvelle version du dataset au complet.
"""

from dask.graph_manipulation import checkpoint

from .data import (
    force_sync,
    verify_preprocess
)
from .train import train
from ..configs import ProjectConfig

def get_task_graph(project_config: ProjectConfig) -> dict:
    dag = {
        "force_sync": (force_sync, project_config.paths),
        "verify_preprocess": (verify_preprocess, 
                              project_config.paths, 
                              project_config.preprocess),
        "train": (train, project_config, "verify_preprocess"),
    }

    return dag
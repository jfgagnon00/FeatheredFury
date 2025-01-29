import numpy as np


from ffury.configs import ProjectConfig
from numpy.typing import NDArray
from pathlib import Path
from typing import (
    Any,
    Union
)


# TODO: workaround dependance sur model custom
#       a refactorer
def _load_model(project_config: ProjectConfig) -> Any:
    filename = Path.joinpath(project_config.paths.MODELS_DIR, "Model.keras")
    if Path.is_file(filename):
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from keras.models import load_model
        from ._KerasBaselineSegmentFeatures import _KerasBaselineSegmentFeatures
        from ._KerasCNNSegmentFeatures import _KerasCNNSegmentFeatures
        return load_model(filename)
    else:
        raise ValueError(f"{filename} n'existe pas")

def _predict_from_probabilities(y_true: NDArray = None,
                                y_pred: NDArray = None,
                                thresholds: Union[float, NDArray] = 0.5) -> NDArray:
    """
    Gere la classe "unknown" qui est implicite. Les predictions faites par les 
    modeles sont assumes faite de classes independantes. Ce qui veut dire que
    sigmoid est la fonction d'activation. Donc, somme des probabilites != 1.0.
    Donc, il est possible que y_true ne contienne que des 0. C'est la classe
    "unknown" implicite.

    Parametres:
        y_true: les vraies probabilites (tenseur contenant uniquement 0 ou 1)
                assume one not encoded
        y_pred: les probabilites de predictions (tenseur contenant des valeurs entre [0, 1])
                assume one not encoded
        thresholds: thresholds pour convertir probabilites de prediction en classes

    Retour:
        tenseur avec les classes predites (incluant la classe "unknown"). La valeur de 
        la classe "unknown" est toujours nombre de colonnes dans les probabilites + 1
        
    Note:
        Un appel a cette fonction assume y_true OU (y_pred et thresholds). Pas les deux.
    """
    if not y_true is None:
        unknown_idx = y_true.shape[-1] + 1
        y_true_idx = np.argmax(y_true, axis=-1)
        y_true_invalid = np.sum(y_true, axis=-1) == 0
        y_true_idx[y_true_invalid] = unknown_idx
        return y_true_idx

    if not y_pred is None and \
       not thresholds is None:
        unknown_idx = y_pred.shape[-1] + 1
        y_pred_idx = np.argmax(y_pred, axis=-1)
        if isinstance(thresholds, float):
            y_pred_invalid = y_pred[np.arange(y_pred.shape[0]), y_pred_idx] <= thresholds
        else:
            y_pred_invalid = y_pred[np.arange(y_pred.shape[0]), y_pred_idx] <= thresholds[y_pred_idx]
        y_pred_idx[y_pred_invalid] = unknown_idx

        return y_pred_idx

    raise ValueError("Parametres invalides")

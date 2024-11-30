from typing import Any

from ..configs import TrainParameters


def keras_optimizer(parameters: TrainParameters) -> Any:
    """
    Retourne l'optimizer correspondant aux parametres
    """
    # cet import est extremement lent - sortir de l'entete
    # https://github.com/keras-team/keras/issues/7408
    from keras.optimizers import Adam

    if parameters.optimizer.lower() == "adam":
         return Adam(learning_rate=parameters.learning_rate)
    
    raise ValueError(f"Optimizer {parameters.optimizer} non reconnu")
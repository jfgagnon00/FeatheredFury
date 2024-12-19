from typing import Any

from ffury.configs import TrainParameters

def keras_loss(parameters: TrainParameters) -> Any:
    """
    Retourne le loss keras correspondant aux parametres
    """
    # ces imports sont extremement lent - sortir de l'entete
    # https://github.com/keras-team/keras/issues/7408
    from keras.losses import SparseCategoricalCrossentropy
    from keras.losses import BinaryCrossentropy

    loss = parameters.loss.lower()

    if loss == "sparse_categorical_crossentropy":
        return SparseCategoricalCrossentropy(from_logits=False)

    if loss == "binary_crossentropy":
        return BinaryCrossentropy(from_logits=False)

    raise ValueError(f"Loss {parameters.loss} non reconnu")
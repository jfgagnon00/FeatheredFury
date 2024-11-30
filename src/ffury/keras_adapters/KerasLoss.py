from typing import Any

from ..configs import TrainParameters

def keras_loss(parameters: TrainParameters) -> Any:
     """
     Retourne l'optimizer correspondant aux parametres
     """
     # cet import est extremement lent - sortir de l'entete
     # https://github.com/keras-team/keras/issues/7408
     from keras.losses import SparseCategoricalCrossentropy

     if parameters.loss.lower() == "sparse_categorical_crossentropy":
          return SparseCategoricalCrossentropy(from_logits=False)

     raise ValueError(f"Loss {parameters.loss} non reconnu")
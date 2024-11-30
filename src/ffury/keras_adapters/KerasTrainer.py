from pathlib import Path
from typing import (
    Any,
    Callable
)

from ..configs import (
    PathsConfig,
    TrainParameters
)
from ..misc.logging import create_logger
from ..misc.Profile import Profile
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasTrainer:
    """
<<<<<<< HEAD
    Encapsule boucle d'entrainement avec Keras.

    LIMITATION: Il est possible que python lance une erreur 'Too many file open'
                Je ne sais pas encore quel est la source du probleme mais un workaround
                est de hausser la limite avec 'ulimit -n 4096'.
=======
    Encapsule boucle d'entrainement avec Keras
>>>>>>> e1f6f1a (Stub metriques par epoque)
    """
    def __call__(self,
                 paths: PathsConfig,
                 parameters: TrainParameters,
                 metrics: Callable,
                 model: Any, 
                 x_train: Any,
                 y_train: Any,
                 x_valdation: Any,
                 y_valdation: Any,) -> None:
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from tensorflow.config import list_physical_devices
        from keras.callbacks import ModelCheckpoint
        from tqdm.keras import TqdmCallback
        from .KerasMetricCallback import KerasMetricCallback

        logger = create_logger(file=__file__)

        logger.info("Device disponible")
        logger.info([f"{d.device_type}, {d.name}" for d in list_physical_devices()])

        model_checkpoint = Path.joinpath(paths.MODELS_DIR, model.name + "-{epoch:03d}.keras")
        model_checkpoint.parent.mkdir(exist_ok=True, parents=True)

        with Profile() as profile:
            model.fit(x_train, y_train,
                      epochs=parameters.epochs,
                      batch_size=parameters.batch_size,
                      validation_data=(x_valdation, y_valdation),

                      # simplifier logging
                      verbose=0,
                      callbacks=[TqdmCallback(),
                                 KerasMetricCallback(x_train, y_train,
                                                     x_valdation, y_valdation,
                                                     metrics),
                                #  ModelCheckpoint(str(model_checkpoint),
                                #                  monitor="val_accuracy",
                                #                  mode="max",
                                #                  verbose=0,
                                #                  save_freq="epoch",
                                #                  save_best_only=False),
                                ])

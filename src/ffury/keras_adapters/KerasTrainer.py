from pathlib import Path
from typing import (
    Any,
    Callable,
    List
)

from ..configs import (
    PathsConfig,
    TrainParameters
)
from ..misc.ITrainable import ITrainable
from ..misc.IMeasurable import IMeasurable
from ..misc.logging import create_logger
from ..misc.Profile import Profile
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasTrainer(ITrainable):
    """
    Encapsule boucle d'entrainement avec Keras.
    """
    def __call__(self,
                 paths: PathsConfig,
                 parameters: TrainParameters,
                 metrics: IMeasurable,
                 model: Any, 
                 class_labels: List[str],
                 x_train: Any,
                 y_train: Any,
                 x_valdation: Any,
                 y_valdation: Any,) -> None:
        # ces imports sont extremement lent - sortir de l'entete
        # https://github.com/keras-team/keras/issues/7408
        from tensorflow.config import list_physical_devices
        from tqdm.keras import TqdmCallback

        from .KerasCallback import KerasCallback

        logger = create_logger(file=__file__)

        logger.info("Device(s) disponible")
        logger.info([f"{d.device_type}, {d.name}" for d in list_physical_devices()])

        # model_checkpoint = Path.joinpath(paths.MODELS_DIR, model.name + "-{epoch:03d}.keras")
        # model_checkpoint.parent.mkdir(exist_ok=True, parents=True)

        with Profile() as profile:
            model.fit(x_train, y_train,
                      epochs=parameters.epochs,
                      batch_size=parameters.batch_size,
                      validation_data=(x_valdation, y_valdation),

                      # simplifier logging
                      verbose=0,
                      callbacks=[TqdmCallback(),
                                 KerasCallback(class_labels,
                                               x_train, y_train,
                                               x_valdation, y_valdation,
                                               metrics)
                                ])

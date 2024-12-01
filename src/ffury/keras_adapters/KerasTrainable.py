from pathlib import Path
from typing import (
    Any,
    List
)

from ..configs import (
    PathsConfig,
    TrainParameters
)
from ..misc.ITrainable import ITrainable
from ..misc.IMeasurable import IMeasurable
from ..misc.logging import create_logger
from ..neptune import NeptuneRun
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasTrainable(ITrainable):
    """
    Encapsule boucle d'entrainement avec Keras.
    """
    def __call__(self,
                 run: NeptuneRun,
                 paths: PathsConfig,
                 parameters: TrainParameters,
                 measurable: IMeasurable,
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

        run.log_model_infos(model.get_config())

        logger = create_logger(file=__file__)
        logger.info("Device(s) disponible")
        logger.info([f"{d.device_type}, {d.name}" for d in list_physical_devices()])

        # model_checkpoint = Path.joinpath(paths.MODELS_DIR, model.name + "-{epoch:03d}.keras")
        # model_checkpoint.parent.mkdir(exist_ok=True, parents=True)

        callback = KerasCallback(class_labels,
                                 x_train, y_train,
                                 x_valdation, y_valdation,
                                 run,
                                 measurable)

        model.fit(x_train, y_train,
                  epochs=parameters.epochs,
                  batch_size=parameters.batch_size,
                  validation_data=(x_valdation, y_valdation),
                  verbose=0,
                  callbacks=[TqdmCallback(), callback])
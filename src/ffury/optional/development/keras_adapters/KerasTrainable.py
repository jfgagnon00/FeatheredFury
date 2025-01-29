from pathlib import Path
from typing import (
    Any,
    List
)

from ffury.configs import (
    PathsConfig,
    TrainParameters
)
from ffury.misc.ITrainable import ITrainable
from ffury.misc.IMeasurable import IMeasurable
from ffury.misc.logging import create_logger
from ffury.yaml.yaml_decorators import YamlDeserializable

from ..neptune import NeptuneRun


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
                 x_train: Any,
                 y_train: Any,
                 x_valdation: Any,
                 y_valdation: Any,
                 x_test: Any,
                 y_test: Any,) -> None:
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
        model_checkpoint = Path.joinpath(paths.MODELS_DIR, model.name + ".keras")
        model_checkpoint.parent.mkdir(exist_ok=True, parents=True)

        callback = KerasCallback(x_train, y_train,
                                 x_valdation, y_valdation,
                                 run,
                                 measurable,
                                 str(model_checkpoint))

        model.fit(x_train, y_train,
                  epochs=parameters.epochs,
                  batch_size=parameters.batch_size,
                  validation_data=(x_valdation, y_valdation),
                  verbose=0,
                  callbacks=[TqdmCallback(), callback])

        if not callback.best_model_checkpoint is None:
            run.log_best_model(callback.best_model_checkpoint,
                               callback.best_epoch,
                               callback.best_measure_name,
                               callback.best_measure_value)
            
            # aussi noter les metriques sur le data de test apres l'entrainement
            callback.log_test_and_thresholds(parameters.epochs,
                                             x_test, y_test)

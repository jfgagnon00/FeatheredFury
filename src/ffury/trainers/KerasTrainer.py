from pathlib import Path
from keras.callbacks import ModelCheckpoint
from tqdm.keras import TqdmCallback
from typing import (
    Any,
    Callable
)

from ..configs import (
    PathsConfig,
    TrainParameters
)
from ..misc.Profile import Profile
from ..yaml.yaml_decorators import YamlDeserializable


@YamlDeserializable
class KerasTrainer:
    """
    Encapsule boucle d'entrainement avec Keras
    """
    def __init__(self):
        pass

    def __call__(self,
                 paths: PathsConfig,
                 parameters: TrainParameters,
                 metrics: Callable,
                 model: Any, 
                 x_train: Any,
                 y_train: Any,
                 x_valid: Any,
                 y_valid: Any,) -> None:
        
        model_checkpoint = Path.joinpath(paths.MODELS_DIR, "{epoch:03d}.keras")
        model_checkpoint.parent.mkdir(exist_ok=True, parents=True)

        # with Profile() as profile:
        #     history = model.fit(x_train, y_train,
        #                         epochs=parameters.epochs,
        #                         batch_size=parameters.batch_size,
        #                         validation_data=(x_valid, y_valid),

        #                         # simplifier logging
        #                         verbose=0,
        #                         callbacks=[TqdmCallback(),
        #                                    ModelCheckpoint(str(model_checkpoint),
        #                                                    monitor="val_f1",
        #                                                    mode="max",
        #                                                    verbose=0,
        #                                                    save_freq="epoch",
        #                                                    save_best_only=False),
        #                                   ])

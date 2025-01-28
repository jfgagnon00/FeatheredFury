from ffury.configs import ProjectConfig
from pathlib import Path
from typing import Any


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

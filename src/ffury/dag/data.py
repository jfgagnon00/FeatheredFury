import subprocess

from pathlib import Path

from ..configs import (
    PathsConfig,
    PreprocessConfig
)
from ..misc.logging import create_logger


def force_sync(paths_config: PathsConfig) -> bool:
    """
    S'assure que le data est syncer. Retourne true pour dire 
    que la tache s'est execute.
    """
    logger = create_logger(file=__file__)
    result = subprocess.run(["dvc", "status", "--quiet"], 
                            check=False, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        logger.info("Donnees sont a jour")
        return False

    logger.info("Sync dvc")
    result = subprocess.run(["dvc", "pull", "--force"], 
                            check=False, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    logger.info(result.stdout.decode("utf-8"))
    return True

def verify_preprocess(paths_config: PathsConfig,
                          preprocess_config: PreprocessConfig) -> bool:
    """
    Valide que le dataset preprocesse correspond a la config. Lance
    une exception si ce n'est pas le cas
    """
    logger = create_logger(file=__file__)

    filename = Path.joinpath(paths_config.DATA_DIR, "data_preprocessed.md5")
    with open(filename, "r") as file:
        md5 = file.readline().strip()

    if preprocess_config.md5() != md5:
        raise ValueError(f"Data preprocessee ne semble pas corresponde aux parametres courant")

    logger.info("Data preprocessee valide")
    return True
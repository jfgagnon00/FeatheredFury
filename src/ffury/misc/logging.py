import logging

from pathlib import PurePath
from typing import Optional

def logger_name_from_file(filename: str) -> str:
    """
    Utilitaire pour uniformiser le noms des loggers a partir d'un nom de fichier
    """
    root = PurePath(__file__).parents[1]
    path = PurePath(filename)
    path = path.relative_to(root)
    return str(path)

def create_logger(name: str = None,
                  file: str = None,
                  verbose: bool = True) -> Optional[logging.Logger]:
    if not file is None:
        name = logger_name_from_file(file)

    if not name is None:
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.disabled = not verbose
        return logger

    return None

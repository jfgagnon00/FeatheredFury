import logging

from io import StringIO
from pathlib import PurePath
from pprint import pprint
from typing import Optional

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

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
        datefmt = DATE_FORMAT
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        return logger

    return None

def pretty_format(object: object, *args, **kwargs) -> str:
    """
    Format objet a l'aide de pprint dans une string et la retourne
    """
    with StringIO() as stream:
        pprint(object=object,
               stream=stream,
               *args,
               **kwargs)
        return stream.getvalue()

from datetime import datetime
from h5py import (
    File,
    string_dtype
)

_KEY_SEPARATOR = "/"
_STRING_ENCODING = "utf8"
_STRING_DTYPE = string_dtype(encoding=_STRING_ENCODING)

_VERSION_MAJOR = 0
_VERSION_MINOR = 0
_VERSION_BUILD = 0

VERSION_KEY = "version"
VERSION_NUMBER_ATTRIBUT = "version"
VERSION_TIMESTAMP_ATTRIBUT = "timestamp"

def _write_version(file: File) -> None:
    group = file.create_group(VERSION_KEY)
    group.attrs[VERSION_NUMBER_ATTRIBUT] = version().encode(_STRING_ENCODING)
    # group.attrs[VERSION_TIMESTAMP_ATTRIBUT] = datetime.now()

def version():
    return f"{_VERSION_MAJOR}.{_VERSION_MINOR}.{_VERSION_BUILD}"

def create_file(filename: str,
                mode: str) -> File:
    file = File(filename, mode=mode)
    _write_version(file)
    return file

def join_keys(*args):
    return _KEY_SEPARATOR.join(args)
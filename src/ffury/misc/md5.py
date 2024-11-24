from hashlib import md5 as hash_md5
from typing import Iterable

def md5_from_iterable(iterable : Iterable) -> str:
    """
    Calcule le md5 de l'ensemble des elements d'une liste
    """
    hash = hash_md5()
    for i in iterable:
        hash.update( str(i).encode() )
    return hash.hexdigest()

def md5_from_object(object_ : any) -> str:
    """
    Calcule le md5 des proprietes trouves par var()
    """
    attributes = vars(object_)
    hash = hash_md5()
    for k in sorted(attributes.keys()):
        value = attributes[k]
        hash.update( str(value).encode() )
    return hash.hexdigest()

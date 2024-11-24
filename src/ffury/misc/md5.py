from hashlib import md5 as hash_md5

def md5(object_ : any) -> str:
    """
    Calcule le md5 des proprietes trouves par var()
    """
    attributes = vars(object_)
    hash = hash_md5()
    for k in sorted(attributes.keys()):
        value = attributes[k]
        hash.update( str(value).encode() )
    return hash.hexdigest()
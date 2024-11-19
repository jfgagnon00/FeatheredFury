import yaml

from hashlib import md5
from inspect import isclass

from ..misc.MetaObject import MetaObject

def _md5(instance):
    """
    Calcule le md5 des proprietes trouves par var()
    """
    attributes = vars(instance)
    hash = md5()
    for k in sorted(attributes.keys()):
        value = attributes[k]
        hash.update( str(value).encode() )
    return hash.hexdigest()

def tag_from_class(cls):
    """
    Utilistaire pour construire un tag a partir d'un type.
    ex:
        - module ffury.configs.GlobalConfig, classe GlobalConfig: 
          tag => "!ffury.configs.GlobalConfig"  

        - module ffury.configs.Misc, classe GlobalConfig: 
          tag => "!ffury.configs.Misc.GlobalConfig"
    """
    cls_name = cls.__name__
    cls_module = cls.__module__

    if cls_module == "__main__":
        return f"!{cls_name}"
    
    if cls_module.endswith(cls_name):
        return f"!{cls_module}"
    
    return f"!{cls_module}.{cls_name}"

def YamlTag(tag):
    """
    Decorateur pour deserialiser un tag yaml
    """
    def WrapperYamlCtor(deserializer):
        yaml.add_constructor(tag, deserializer)
        deserializer.yaml_tag = tag

        return deserializer

    if tag is None or not isinstance(tag, str):
        raise ValueError("tag must be a string")

    return WrapperYamlCtor

def YamlDeserializable(cls):
    """
    Decorateur pour encapsuler yaml deserialization. Le tag est 
    deduit par le type
    """
    if not isclass(cls):
        raise ValueError("YamlSerializable can only be used on class")
    
    def YamlSimpleDeserialzation(loader, node):
        instance = cls()
        attributes = loader.construct_mapping(node)
        MetaObject.override_from_dict(instance, attributes)
        return instance
    
    tag = tag_from_class(cls)
    yaml.add_constructor(tag, YamlSimpleDeserialzation)
    cls.yaml_tag = tag
    
    # ajout hashing md5 pour chaque yaml deserialisable
    cls.md5 = lambda self: _md5(self)

    return cls

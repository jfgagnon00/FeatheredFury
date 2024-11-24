import yaml

from inspect import isclass

from ..misc.MetaObject import MetaObject

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

    return cls

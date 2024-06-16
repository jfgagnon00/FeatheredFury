import yaml

class MetaObject(object):
    """
    Utilitaire pour transformer un dictionnaire
    en object python. Les clefs deviennent des
    attributs.
    """
    def __init__(self, attributes):
        MetaObject.override_from_dict(self, attributes)

    def __contains__(self, key):
        """
        Commodite pour verifier si key est contenu dans cet object
        """
        return key in self.__dict__

    def __iter__(self):
        """
        Commodite pour iterer les proprietes de cet objet
        """
        return iter(vars(self).items())

    def as_dict(self) -> dict:
        """
        Commodite pour convertir cet objet en dictionnaire
        """
        return vars(self)

    @classmethod
    def from_dict(cls, attributes):
        return MetaObject(attributes)

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls.from_dict(kwargs)

    @classmethod
    def from_yaml(cls, filename):
        try:
            with open(filename) as f:
                attributes = yaml.load(f, yaml.Loader)
        except Exception as e:
            print(e)
            return None
        else:
            return cls.from_dict(attributes)

    @classmethod
    def override_from_kwargs(cls, instance, **kwargs):
        cls.override_from_dict(instance, kwargs)

    @classmethod
    def override_from_dict(cls, instance, attributes):
        if isinstance(attributes, dict):
            instance.__dict__.update(attributes)
        else:
            raise RuntimeError("MetaObject can only "
                               "be constructed from dict")

    @classmethod
    def override_from_yaml(cls, instance, filename):
        try:
            with open(filename) as f:
                attributes = yaml.load(f, yaml.Loader)
        except Exception as e:
            print(e)
            raise RuntimeError("Could not create attributes for MetaObject")
        else:
            cls.override_from_dict(instance, attributes)

    @classmethod
    def override_from_object(cls, instance, object):
        cls.override_from_dict(instance, vars(object))

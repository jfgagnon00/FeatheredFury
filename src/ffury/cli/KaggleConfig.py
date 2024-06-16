from ..configs import MetaObject

class KaggleConfig(MetaObject):
    """
    Encapsule les proprietes globales du dataset Kaggle
    """
    def __init__(self):
        self.competition = ""

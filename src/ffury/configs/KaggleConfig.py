from .MetaObject import MetaObject

class KaggleConfig(MetaObject):
    """
    Encapsule les proprietes globales du dataset Kaggle
    """
    def __init__(self):
        self.competition = ""

    @property
    def csvFilename(self):
        return "train_metadata.csv"

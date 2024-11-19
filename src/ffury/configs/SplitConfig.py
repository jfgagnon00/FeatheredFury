from ..yaml import YamlDeserializable


@YamlDeserializable
class SplitConfig:
    """
    Encapsule les proprietes pour le split (train/test)

    Notes:
        validation est ce qui reste apres train/test
    """
    def __init__(self):
        self.split_train_size = 0
        self.split_test_size = 0

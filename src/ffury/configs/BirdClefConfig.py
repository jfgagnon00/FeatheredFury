from ..yaml import YamlDeserializable


@YamlDeserializable
class BirdClefConfig:
    """
    Encapsule les proprietes globales du dataset BirdCLEF 2023
    """
    def __init__(self):
        self.competition = "birdclef-2023"

    @property
    def bird_metadata_url(self):
        """
        Ajouter primary_label a cet url pour obtenir metadata
        au sujet d'un oiseau en particulier
        """
        return "https://ebird.org/species/"

    @property
    def url(self):
        """
        Url pointant sur la des
        """
        return "https://www.kaggle.com/competitions/" + self.competition

    @property
    def data_description_url(self):
        return self.url + "/data"

    @property
    def csv_filename(self):
        return "train_metadata.csv"
    
    @property
    def audio_dir(self):
        return "train_audio"

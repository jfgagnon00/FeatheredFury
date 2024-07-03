from pandas import read_csv
from pathlib import Path

def load_dataset_raw(config):
    """
    Utilitaire pour loader dataset raw
    """
    filename = Path.joinpath(config.project.DATA_RAW_DIR, 
                             config.dataset.csvFilename)
    return read_csv(filename)

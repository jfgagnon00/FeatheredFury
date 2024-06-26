import click
import pathlib
import zipfile

from . import ConfigDecorator
from ..misc import Logger
from tqdm import tqdm

@click.command()
@click.option("--force", is_flag=True, default=False, show_default=True, help="Force download")
@click.option("--verbose/--no-verbose", default=True, show_default=True, help="Affiche progression")
@click.option("--clear", is_flag=True, default=False, show_default=True, help="Efface .zip intermediaire")
@click.option("--path", type=click.Path(), help="Override path de download")
@ConfigDecorator
def dataset(config, force, verbose, clear, path):
    """
    Encapsule installation du dataset venant de Kaggle
    """
    logger = Logger(verbose)

    if path is None:
        path = config.project.dataRawDir

    competition = config.dataset.competition
    _download(competition, path, force, verbose)

    # decompression dataset
    filename = pathlib.Path(path).joinpath(f"{competition}.zip")

    logger.log("Decompression", filename)
    _decompress(filename, path)

    if clear:
        logger.log("Clear", filename)
        pathlib.Path.unlink(filename)

def _download(competition, path, force, verbose):
    # import du module fait authentication automatiquement
    import kaggle
    kaggle.api.competition_download_cli(competition=competition,
            # competition_opt=None,
            # file_name=None,
            path=path,
            force=force,
            quiet=not verbose)
    
def _decompress(filename, path):
    with zipfile.ZipFile(filename, "r") as zip:
        names = zip.namelist()
        for name in tqdm(names, total=len(names), bar_format="{l_bar}{bar}"):
            zip.extract(name, path=path)

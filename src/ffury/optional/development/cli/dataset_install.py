import click
import zipfile

from ffury.cli import ProjectConfigDecorator
from ffury.misc.logging import create_logger

from .dataset import dataset_group
from pathlib import Path
from tqdm import tqdm

@dataset_group.command()
@click.option("--force", is_flag=True, default=False, show_default=True, help="Force download")
@click.option("--verbose/--no-verbose", default=True, show_default=True, help="Affiche progression")
@click.option("--delete", is_flag=True, default=False, show_default=True, help="Efface .zip intermediaire")
@click.option("--path", type=click.Path(), help="Override path de download")
@ProjectConfigDecorator
def install(config, force, verbose, delete, path):
    """
    Installation du dataset venant de Kaggle
    """
    logger = create_logger(file=__file__, verbose=verbose)

    if path is None:
        path = config.paths.DATA_RAW_DIR

    competition = config.dataset.competition
    _download(competition, path, force, verbose)

    # decompression dataset
    filename = Path(path).joinpath(f"{competition}.zip")

    logger.info(f"Decompression '{filename}'")
    _decompress(filename, path)

    if delete:
        logger.info(f"Efface '{filename}'")
        filename.unlink()

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

import click
import neptune
import os

from ffury.cli import ProjectConfigDecorator
from ffury.configs import ProjectConfig
from ffury.misc.logging import create_logger
from pathlib import Path

from .neptune import neptune_group
from ..neptune.NeptuneRun import NeptuneRun


@neptune_group.command()
@click.argument("tag")
@ProjectConfigDecorator
def sync_model(project_config: ProjectConfig,
               tag: str) -> None:
    """
    Download un model se trouvant sur Neptune AI.
    """
    with NeptuneRun(project_config,
                    upload=False,
                    tags=[tag]) as run:
        destination = Path.joinpath(project_config.paths.MODELS_DIR, "Model.keras")
        destination = str(destination)
        run.save_best_model(destination)

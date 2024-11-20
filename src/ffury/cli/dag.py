import click

from dask.threaded import get
from dask.optimization import cull

from . import ProjectConfigDecorator
from ..configs import ProjectConfig
from ..dag import get_task_graph
from ..misc.logging import create_logger


@click.command()
@click.argument("task", type=str, default="")
@ProjectConfigDecorator
def dag(project_config: ProjectConfig, 
        task: str) -> None:
    """
    Encapsule les taches du dag.
    """
    logger = create_logger(file=__file__)
    tasks = get_task_graph(project_config)
    if not task in tasks:
        message = f"'{task}' n'existe pas\n\n"
        message += "Taches disponible:\n"
        for k in sorted(tasks.keys()):
            message += f"    {k}\n"
        logger.error(message)
        return

    logger.info(f"Execution de '{task}'")
    tasks, _ = cull(tasks, task)
    get(tasks, task)
    logger.info(f"Execution de '{task}' termine")

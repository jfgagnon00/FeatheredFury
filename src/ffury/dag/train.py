from ..configs import ProjectConfig
from ..misc.logging import create_logger


def train(project_config: ProjectConfig, *args) -> None:
    logger = create_logger(file=__file__)
    logger.info("Train")
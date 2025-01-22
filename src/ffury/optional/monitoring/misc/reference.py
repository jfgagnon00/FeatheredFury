from ffury.configs import ProjectConfig
from pathlib import Path

def get_filename(project_config: ProjectConfig) -> str:
    return Path.joinpath(project_config.paths.BUILD_DIR, "monitoring_features.csv")

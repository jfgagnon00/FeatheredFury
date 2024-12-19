import neptune

from datetime import datetime
from json import dumps
from os import environ
from typing import (
    Any,
    Dict,
    List,
    Tuple
)

from ffury.configs import ProjectConfig
from ffury.misc.logging import DATE_FORMAT

from ..dataset import IndexedDataset


class NeptuneRun:
    """
    Encapsule la communication avec Neptune.AI lors d'une experimentation
    """
    def __init__(self, 
                 project_config: ProjectConfig) -> None:
        name, tags = NeptuneRun._run_infos_create()
        self._run = NeptuneRun._run_create(project_name=project_config.paths.PROJECT_NAME,
                                           run_name=name,
                                           tags=tags)
        self._log_configs(project_config)

    def log_data_infos(self, 
                       train: IndexedDataset, 
                       validation: IndexedDataset) -> None:
        self._run["data/train/spectrogram_groups_shape"] = str(train.spectrogram_groups.shape)
        self._run["data/train/md5/preprocessed"] = train.md5_preprocessed
        self._run["data/train/md5/indexed"] = train.md5_indexed

        self._run["data/validation/spectrogram_groups_shape"] = str(validation.spectrogram_groups.shape)
        self._run["data/validation/md5/preprocessed"] = validation.md5_preprocessed
        self._run["data/validation/md5/indexed"] = validation.md5_indexed

    def log_model_infos(self, model_infos: Dict) -> None:
        self._run["model/infos"] = dumps(model_infos, indent=4)

    def log_best_model(self, 
                       model_checkpoint: str,
                       epoch: int,
                       measure_name: str,
                       measure_value: float) -> None:
        self._run["model/best_model"].upload(model_checkpoint)
        self._run["model/best_epoch"] = epoch
        self._run["model/best_metric_name"] = measure_name
        self._run["model/best_metric_value"] = measure_value

    def append_measures(self, 
                        epoch: int,
                        measures: Dict):
        for name, value in measures.items(): 
            self._run[f"metrics/{name}"].append(value, step=epoch)

    def log_duration(self, duration: float):
        self._run["metrics/duration"] = duration
    
    def _log_configs(self, 
                     project_config: ProjectConfig) -> None:
        self._run["config/num_classes"] = project_config.num_classes
        self._run["config/md5/preprocessed"] = project_config.preprocess.split_sampling_md5()
        self._run["config/md5/indexed"] = project_config.preprocess.spectrogram_md5()
        self._run["config/dataset"] = vars(project_config.dataset)
        self._run["config/preprocess"] = vars(project_config.preprocess)
        self._run["config/train/model_factory"] = type(project_config.train.model_factory).__name__
        self._run["config/train/trainable"] = type(project_config.train.trainable).__name__
        self._run["config/train/measurable"] = type(project_config.train.measurable).__name__
        self._run["config/train/parameters"] = vars(project_config.train.parameters)

    # Utilitaire pour utilisation avec with()
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._run.stop()

    @staticmethod
    def _run_infos_create() -> Tuple[str, List[str]]:
        name = NeptuneRun._username()
        date = datetime.now().strftime(DATE_FORMAT)
        tags = []

        if "BUILD_MACHINE" in environ:
            tags.append("ci")
        else:
            tags.append("local")

        return f"{name}-{date}", tags

    @staticmethod
    def _run_create(project_name: str,
                    run_name: str = None,
                    tags: List[str] = None) -> neptune.Run:
        api_token = environ["NEPTUNE_API_TOKEN"]

        if len(api_token) == 0:
            raise ValueError("NEPTUNE_API_TOKEN non defini")

        return neptune.init_run(
            project=f"{project_name}/{project_name}",
            api_token=api_token,
            name=run_name,
            tags=tags,
            source_files=[],
            git_ref=False,
            capture_stdout=False,
            capture_stderr=False,
            capture_hardware_metrics=True)
    
    @staticmethod
    def _username():
        if "USER" in environ:
            return environ["USER"]

        if "USERNAME" in environ:
            return environ["USERNAME"]
        
        return "unknown-user"

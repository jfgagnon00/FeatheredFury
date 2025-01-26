import neptune

from datetime import datetime
from json import dumps
from neptune.utils import stringify_unsupported
from os import environ
from typing import (
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
                 project_config: ProjectConfig,
                 upload: bool = True,
                 tags: List[str] = None) -> None:
        if upload:
            name, tags_ = NeptuneRun._run_infos_create()

            if not tags is None:
                tags_ += tags

            self._run = NeptuneRun._run_create_for_upload(project_config,
                                                          run_name=name,
                                                          tags=tags_)
            self._log_configs(project_config)
        else:
            self._run = NeptuneRun._run_create_for_download(project_config,
                                                            tags=tags)

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

    def save_best_model(self,
                         destination: str) -> None:
        self._run["model/best_model"].download(destination=destination)

    def append_measures(self, 
                        epoch: int,
                        measures: Dict):
        for name, value in measures.items(): 
            self._run[f"metrics/{name}"].append(value, step=epoch)

    def log_model_thresholds(self, thresholds: List[float]) -> None:
        self._run["model/thresholds"] = stringify_unsupported(thresholds)

    def log_duration(self, duration: float):
        self._run["metrics/duration"] = duration
    
    def _log_configs(self, 
                     project_config: ProjectConfig) -> None:
        self._run["config/num_classes"] = project_config.num_classes
        self._run["config/md5/preprocessed"] = project_config.preprocess.split_sampling_md5()
        self._run["config/md5/indexed"] = project_config.preprocess.spectrogram_md5()
        self._run["config/dataset"] = stringify_unsupported(vars(project_config.dataset))
        self._run["config/preprocess"] = stringify_unsupported(vars(project_config.preprocess))
        self._run["config/train/model_factory"] = type(project_config.train.model_factory).__name__
        self._run["config/train/trainable"] = type(project_config.train.trainable).__name__
        self._run["config/train/measurable"] = type(project_config.train.measurable).__name__
        self._run["config/train/parameters"] = stringify_unsupported(vars(project_config.train.parameters))

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
    def _run_create_for_upload(project_config: ProjectConfig,
                               run_name: str = None,
                               tags: List[str] = None) -> neptune.Run:
        api_token = environ["NEPTUNE_API_TOKEN"]

        if len(api_token) == 0:
            raise ValueError("NEPTUNE_API_TOKEN non defini")

        return neptune.init_run(
            project=NeptuneRun._projectname(project_config),
            api_token=api_token,
            name=run_name,
            tags=tags,
            source_files=[],
            git_ref=True,
            capture_stdout=False,
            capture_stderr=False,
            capture_hardware_metrics=True)
    
    def _run_create_for_download(project_config: ProjectConfig,
                                 tags: List[str] = None) -> neptune.Run:
        api_token = environ["NEPTUNE_API_TOKEN"]

        if len(api_token) == 0:
            raise ValueError("NEPTUNE_API_TOKEN non defini")

        project = neptune.init_project(project=NeptuneRun._projectname(project_config),
                                       api_token=api_token,
                                       mode="read-only")
        query = []
        for tag in tags:
            q = f"(`sys/group_tags`:stringSet CONTAINS '{tag}')"
            query.append(q)
        query = " AND ".join(query)

        runs_df = project.fetch_runs_table(query=query).to_pandas()

        if len(runs_df) == 0:
            raise ValueError(f"{tags} n'ont pas ete trouve")

        if len(runs_df) > 1:
            raise ValueError(f"Plusieurs run on les tags {tags}")

        return neptune.init_run(
            project=NeptuneRun._projectname(project_config),
            api_token=api_token,
            with_id=runs_df.loc[0, "sys/id"],
            mode="read-only")
    
    @staticmethod
    def _username():
        if "USER" in environ:
            return environ["USER"]

        if "USERNAME" in environ:
            return environ["USERNAME"]
        
        return "unknown-user"

    @staticmethod
    def _projectname(project_config: ProjectConfig) -> str:
        return f"{project_config.paths.PROJECT_NAME}/{project_config.paths.PROJECT_NAME}"

from setuptools import find_namespace_packages, setup

def _dependencies_core():
    return [
        "click==8.1.7",
        "dask[distributed]==2024.7.1",
        "flasgger==0.9.7.1",
        "flask==3.1.0",
        "keras==3.3.3",
        "librosa==0.10.2.post1",
        "matplotlib==3.9.0",
        "neptune==1.10.4",
        "numpy<2", # limitation librosa
        "pyyaml==6.0.1",
        "tensorflow==2.16.1",
        "requests==2.32.3",
    ]

def _dependencies_development():
    return [
        "dvc-gdrive==3.0.1",
        "dvc==3.51.3",
        "h5py==3.11.0",
        "tqdm==4.66.4",
    ]

def _dependencies_local():
    return [
        "ipykernel==6.29.5",
        "ipywidgets==8.1.3",
        "jupyterlab==4.2.3",
        "kaggle==1.6.14",
        "seaborn==0.13.2",
        "tensorflow-metal==1.1.0; sys_platform == 'darwin'"
    ]

setup(name="feathered-fury",
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      version="0.0.1",
      description="Détection espèce d'oiseau à partir d'une capture audio.",
      author="Jean-Francois Gagnon",
      entry_points={
        "console_scripts": [
            "ffury = ffury.cli:ffury",
        ]},
      install_requires=_dependencies_core(),
      extras_require={
        "development": _dependencies_development(),
        "local": _dependencies_local(),
        "all": _dependencies_development() +  _dependencies_local()
      })

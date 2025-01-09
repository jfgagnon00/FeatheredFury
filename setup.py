from setuptools import find_namespace_packages, setup

def _dependencies_core():
    return [
        "click==8.1.7",
        "pyyaml==6.0.1",
    ]

def _dependencies_ai():
    return [
        "dask[distributed]==2024.7.1",
        "keras==3.3.3",
        "librosa==0.10.2.post1",
        "matplotlib==3.9.0",
        "neptune==1.10.4",
        "numpy<2", # limitation librosa
        "pyyaml==6.0.1",
        "tensorflow==2.17.1",
        "scipy==1.13.1",
    ]

def _dependencies_development():
    return [
        "azure-cli==2.53.1",
        "dvc-gdrive==3.0.1",
        "dvc==3.51.3",
        "h5py==3.11.0",
        "pyopenssl==24.2.1", # fix probleme avec dvc & google drive
        "tqdm==4.66.4",
    ]

def _dependencies_web_core():
    return [
        # TODO: a revoir
        # "azure-identity==1.14.1",
        # "azure-keyvault-secrets==4.7.0",
        # "pyjwt==2.10.1",
        "pandas==2.2.3",
    ]

def _dependencies_application():
    return [
        "flask==3.1.0",
        "requests==2.32.3",
    ]

def _dependencies_service():
    return [
        "flasgger==0.9.7.1",
        "flask==3.1.0",
        "werkzeug==3.1.3",
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
        "development": _dependencies_development() + _dependencies_ai(),
        "application": _dependencies_application() + 
                       _dependencies_web_core(),
        "service": _dependencies_service() + 
                   _dependencies_web_core() + 
                   _dependencies_ai(),
        "all": _dependencies_ai() +
               _dependencies_web_core() +
               _dependencies_development() +  
               _dependencies_application() +
               _dependencies_service() +
               _dependencies_local()
      })

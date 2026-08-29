from setuptools import find_namespace_packages, setup

def _dependencies_core():
    return [
        "click==8.5.0",
        "pyyaml==6.0.3",
    ]

def _dependencies_ai():
    return [
        "dask[distributed]==2026.8.0",
        "keras==3.15.1",
        "librosa==0.11.0",
        "matplotlib==3.11.1",
        "neptune==1.14.0.post2",
        "numpy<2", # limitation librosa
        "pyyaml==6.0.3",
        "tensorflow==2.17.1",
        "scipy==1.14.0",
    ]

def _dependencies_development():
    return [
        "azure-cli==2.89.0",
        "dvc-gdrive==3.0.1",
        "dvc==3.67.1",
        "h5py==3.16.0",
        "tqdm==4.70.0",
    ]

def _dependencies_web_core():
    return [
        "pandas==3.0.5",
    ]

def _dependencies_application():
    return [
        "flask==3.1.3",
        "requests==2.34.2",
    ]

def _dependencies_service():
    return [
        "flasgger==0.9.7.1",
        "flask==3.1.3",
        "werkzeug==3.1.8",
    ]

def _dependencies_monitoring():
    return [
        "azure-cli==2.89.0",
        "azure-storage-blob==12.29.0b1",
        "azure-identity==1.25.3",
        "evidently==0.7.21",
    ]

def _dependencies_local():
    return [
        "ipykernel==7.3.0",
        "ipywidgets==8.1.9",
        "jupyterlab==4.6.3",
        "kaggle==2.2.4",
        "seaborn==0.13.2",
        "tensorflow-metal==1.2.0 ; sys_platform == 'darwin'"
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
      include_package_data=True,
      install_requires=_dependencies_core(),
      extras_require={
        "development": _dependencies_development() + 
                       _dependencies_monitoring() +
                       _dependencies_ai(),
        "application": _dependencies_application() + 
                       _dependencies_web_core(),
        "service": _dependencies_service() + 
                   _dependencies_web_core() + 
                   _dependencies_monitoring() +
                   _dependencies_ai(),
        "monitoring": _dependencies_monitoring(),
        "all": _dependencies_ai() +
               _dependencies_web_core() +
               _dependencies_development() +  
               _dependencies_application() +
               _dependencies_service() +
               _dependencies_local() + 
               _dependencies_monitoring()
      })

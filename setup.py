from setuptools import find_packages, setup

setup(name="feathered-fury",
      package_dir={"": "src"},
      version="0.0.1",
      description="Détection espèce d'oiseau à partir d'une capture audio.",
      author="Jean-Francois Gagnon",
      entry_points={
        "console_scripts": [
            "fury = furycli:fury",
        ]
      })

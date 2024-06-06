from setuptools import find_namespace_packages, setup

setup(name="feathered-fury",
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      version="0.0.1",
      description="Détection espèce d'oiseau à partir d'une capture audio.",
      author="Jean-Francois Gagnon",
      # entry_points={
      #   "console_scripts": [
      #       "ffury = ffury.cli:ffury",
      #   ]
      # }
      )

<div align="center">
  <h1>Feathered Fury</h1>
  <img src="documentation/image/chicken.jpg" width="512">
</div>

## [Installation environment dévelopement](documentation/setup.md)

## Organisation des dossiers
```
   ├── .ci                <- Scripts bash et configurations propres a la gestion du CI
   ├── LICENSE
   ├── README.md          <- The top-level README for developers using this project
   ├── build              <- Destination de tous les resultats temporaires (cree au besoin
   |                         par le pipeline)
   ├── configs            <- Contient toutes les configurations du projet
   ├── data
   │   └── raw            <- The original, immutable data dump.
   ├── initialize.sh      <- Script pour préparer environment virtuel de python
   ├── models             <- Trained and serialized models, model predictions, or model summaries
   ├── playgrounds        <- Experimentation script pythons. Ajout dans repo doit etre explicite.
   ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
   │   │                     the creator's initials, and a short `-` delimited escription, e.g.
   │   └── template_00-user_name-step.ipynb <- Template de notebook
   ├── documentation      <- Documentation et references.
   ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
   ├── setup.py           <- Makes project pip installable (pip install -e .) so src can
   |                         be imported
   └── src                <- Code source utilise pour le projet
```

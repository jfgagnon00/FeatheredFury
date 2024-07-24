<div align="center">
  <h1>Feathered Fury</h1>
  <img src="documentation/image/chicken.jpg" width="512">
</div>

## Liens utiles

* [Installation environment dévelopement](documentation/setup.md)
* [Utilisation](documentation/usage.md)

## Organisation des dossiers
```
   ├── .ci                <- Scripts bash et configurations propres a la gestion du CI
   ├── LICENSE
   ├── README.md          <- README haut niveau pour les developers utilisant ce projet
   ├── build              <- Destination de tous les resultats temporaires (cree au besoin
   |                         par le pipeline)
   ├── configs            <- Contient toutes les configurations du projet
   ├── data
   │   ├── data_raw.csv   <- Le data resultant de l'exploration
       |                     Creee via Jupyter Lab
   |   └── raw            <- Le data original, immutable.
   ├── initialize.sh      <- Script pour préparer environment virtuel de python
   ├── models             <- Trained and serialized models, model predictions, or model summaries
   ├── playgrounds        <- Experimentation script pythons. Ajout dans repo doit etre explicite.
   ├── jupyterlabs        <- Jupyter labs. Naming convention is a number (for ordering),
   │   │                     the creator's initials, and a short `-` delimited escription, e.g.
   │   └── template_00-user_name-step.ipynb <- Template de notebook
   ├── documentation      <- Documentation et references.
   ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
   ├── setup.py           <- Makes project pip installable (pip install -e .) so src can
   |                         be imported
   ├── ffury.yaml         <- Point d'entre pour les configurations globales
   └── src                <- Code source utilise pour le projet
```

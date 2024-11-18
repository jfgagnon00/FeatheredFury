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
   ├── .github            <- Configuration github actions
   ├── LICENSE
   ├── README.md          <- README haut niveau pour les developers utilisant ce projet
   ├── build              <- Destination de tous les resultats temporaires (cree au besoin
   |                         par le pipeline)
   ├── configs            <- Contient toutes les configurations du projet
   ├── data
   │   ├── data_explored.csv.dvc   <- Le data resultant de l'exploration
       |                     Creee via Jupyter Lab
   |   └── raw            <- Le data original, immuable.
   ├── initialize.sh      <- Script pour préparer environment de développement.
   ├── models             <- Modèles entraînés et sérialisés.
   ├── playgrounds        <- Experimentation script pythons. Ajout dans repo doit etre explicite.
   ├── jupyterlabs        <- Jupyter labs. convention de nommage est:
   │   │                     numero avec 2 digits '-' initiale de l'auteur '-' description courte
   │   └── template_00-user_name-step.ipynb <- Template de notebook
   ├── documentation      <- Documentation.
   │   ├── references     <- Publications d'intérêts.
   │   ├── reports        <- Rapports livrés à Bois-de-Boulogne
   ├── playgrounds        <- Partage d'expérimentations. NON INCLU DANS LE PROCESSUS CI/CD. 
   │                         Les commits dans ce répertoire devraient être infréquents.
   ├── requirements.txt   <- Requis pour environment virtuel de python.
   ├── setup.py           <- Makes project pip installable (pip install -e .) so src can
   |                         be imported
   ├── ffury.yaml         <- Point d'entré pour les configurations globales
   └── src                <- Code source utilise pour le projet
       ├── client         <- Application client.
       └── api            <- Api
```

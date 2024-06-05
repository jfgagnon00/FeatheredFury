<div align="center">
  <h1>Feathered Fury</h1>
  <img src="data/image/chicken.jpg" width="512">
</div>

## Installation environment dévelopement

### Accès au suivi de métriques/modèles 
1. Créer un compte [Netpune AI](https://neptune.ai/)
1. Obtenir token d'API
1. Assigner sa valeur à la variable d'environment globale NEPTUNE_API_TOKEN
1. Demander à être ajouté au projet FeatheredFury

### Accès au dataset
1. Créer un compte [Kaggle](https://www.kaggle.com/)
1. Suivre ces [instructions](https://www.kaggle.com/docs/api) pour obtenir un token d'API
1. Copier kaggle.json dans ~/.kaggle/kaggle.json
1. Accepter les règles de [BirdCLEF 2023](https://www.kaggle.com/competitions/birdclef-2023/rules)

### Accès au code
1. S'assurer que python 3 est installer et accessible à la ligne de commande
1. Cloner ce repo
1. A la ligne de commande
```
# nécessaire lors de la première installation seulement
# validation + génération de activate.sh
./initialize.sh

# active environment virtuel
source activate.sh
```

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
   ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for rdering),
   │   │                     the creator's initials, and a short `-` delimited escription, e.g.
   │   └── template_00-user_name-step.ipynb <- Template de notebook
   ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
   ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
   ├── setup.py           <- Makes project pip installable (pip install -e .) so src can
   |                         be imported
   └── src                <- Code source utilise pour le projet
```

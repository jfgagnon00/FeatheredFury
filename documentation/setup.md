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

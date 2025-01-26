### Accès au suivi de métriques/modèles 
1. Créer un compte [Netpune AI](https://neptune.ai/)
1. Obtenir token d'API
1. Assigner sa valeur à la variable d'environment globale NEPTUNE_API_TOKEN
1. Demander à être ajouté au projet FeatheredFury

### Accès au suivi de métriques/production 
1. Créer un compte [Evidently AI](https://www.evidentlyai.com/register)
1. Obtenir token d'API
1. Assigner sa valeur à la variable d'environment globale EVIDENTLY_API_TOKEN
1. Obtenir id de project
1. Assigner sa valeur à la variable d'environment globale EVIDENTLY_PROJECT_ID
1. Demander à être ajouté au projet FeatheredFury

### Accès au dataset
1. Créer un compte [Kaggle](https://www.kaggle.com/)
1. Suivre ces [instructions](https://www.kaggle.com/docs/api) pour obtenir un token d'API
1. Copier kaggle.json dans ~/.kaggle/kaggle.json
1. Accepter les règles de [BirdCLEF 2023](https://www.kaggle.com/competitions/birdclef-2023/rules)

### Accès au code
1. S'assurer que [yq](https://formulae.brew.sh/formula/yq) est installer et accessible
> Notez que sur environment orienté Linux, [yq](https://github.com/mikefarah/yq) peut s'installer via wget.
> Notez que la variable d'environment PATH peut avoir à être modifiée.
1. S'assurer que [ffmpeg](https://www.ffmpeg.org/download.html) est installer et accessible.
> Notez que la variable d'environment PATH peut avoir à être modifiée.
1. S'assurer que python 3 est installer et accessible à la ligne de commande
1. Cloner ce repo
1. A la ligne de commande
```
# nécessaire lors de la première installation seulement
# génération de activate.sh
./initialize.sh

# active environment virtuel
source activate.sh
```

### Management de projet
1. Créer un compte sur [Microsoft Planner](* [Microsoft Plannter | FeatheredFury](https://planner.cloud.microsoft)
1. Demander à être ajouté au projet FeatheredFury

# ML Monitoring

## Besoin a haut niveau
- Notre app n'est pas realtime ; volume d'appels est assumé petit
- Mode batch m'apparait approprié
    - en plus que l'accès au vrai label est plutot restreint

## Solutions possibles

- Prometheus + Grafanna + Evidently
    - Mode de fonctionnement de Prometheus est pull ; mon app est plutot push
    - Demande configuration Azure pour service Prometheus + adapter service au mode pull
    - Demande configuration Azure pour storage
    - Configurer tout ce monde la
    - Faire le query du data dans le temps est simple puisque Prometheus offre un language pour les queries
    - Effectuer le test de drift doit etre fait par notre code anyway
        - donc Prometheus repond plus au besoin de storage et query
        - Grafanna fait des graphes
        - donc pas solution en tant que tel pour trigger le calcul

- **Blob storage sur Azure + cron job sur Github + Evidently**
    - Modifier service pour push data
    - Modifier terraform script pour ajouter account storage
    - Ajouter bout de code pour faire le test de drift
    - Envoyer les resultats sur evidently
    Donc, semble plus en lien avec le mode batch et fit mieux avec notre architecture

## Les tests a implementer
    - Voir NannyML ; il y a un exemple avec classification image
        - en gros Confidence-based Performance Estimation
            - ca va prendre notre data de reference + labels
            - ca va prendre aussi prediciton et label du service

    - Toujours avec NannyML, distribution du data en entree
        (voir liens en email)

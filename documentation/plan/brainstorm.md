- Application
    - Flask
    - Bootstrap pour CSS
    - Deploye avec Heroku/Streamlit/Render/Netlify
        - valider que Heroku est encore disponible
    - Idee a haut niveau
        - user fourni fichier audio (.mp3 ou .ogg) relativement court (< 5MB>)
        - service retourne list avec (espece, temps de detection)
        - feedback user => prediction faite est bonne ou pas
    - Performance
        - Quelques requetes a la minute
        - 500ms pour pour prediction fichier 10 secondes

- Service
    - Flask
        Q1 - comment on accede au modele dans une fois deploye?
        On peut utiliser Google drive ou S3/Azure ; l'idee est que a l'init de l'application lorsqu'elle se deploie, on peut aller "fetcher" ledit modele.
    - Deploiement sur Heroku/Streamlit/Render/Netlify
    - Documentation avec Swagger
    - Securire JWT pour request
    - Tracking des data
        - on garde les fichiers envoyes (data de production)
            - google drive pour le stockage
        - si user envoie feedback, on l'associe a au ficier predit
            - BD Postgres SQL

- CI
    - Environment developpement
        python, dask pour coder 
        dvc + google drive pour tracker data
        neptune ai pour tracker metriques

    - Automatisation
        nos modules offrent interface commande line

    - Flow de travail
        - sur chaque push du main, on re-entraine et on log les metriques sur Neptune AI
            - sur main au complet ou sur les configs + code de modele? ex) changer la documentation devrait-elle re-entrainer le modele?
        - sauvegarde du modele sur NeptuneAI (a investiguer pour limitations)
    - DockerHUB pour environments CI
        - besoin GPU?
    - Utiliser branche pour distinguer Dev/Staging/Prod
    - Utiliser tag pour marquer versions

- Modeles
    - celui du papier (aussi montre dans video youtube)
    - transfer learning vgg ou resnet 

- Gestion projet
    - Trello
        - Etablir des phases pour le projet

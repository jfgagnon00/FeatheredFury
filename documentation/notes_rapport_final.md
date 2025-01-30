# Semaine du 26 janvier 2025

- Complété poc sur monitoring
    - ai décidé d'utiliser test embedding distributions (pas complet mais montre un flow possible)
    - voir Nanny ML avec test sur la confiance des prédictions (prochain monitoring a ajouter)

- Commencé à expérimenter avec l'architecture du modèle
    - Réglé problème d'entraînement - causé par mauvais learning rate et architecture trop simpliste
    - Changer Dummy en BaseLine - finalement a pu servir pour déterminer baseline (voir FEAT-197 Neptune AI)
        - bas F1
    - Implémenté modèle avec CNN - breakthrough sur score F1 (voir FEAT-230 Neptune AI)
        - problème recall Barn Swallow
        - faudrait montrer matrice de confusion a ce stade
    - Réglé probleme classe 'unknown' - gestion de la classe inconnue faisait que Barn Swallow ramassait
                                        les mauvaises classifications (voir FEAT-260 Neptune AI)
        - faudrait montrer matrice de confusion a ce stade
    - Ajout optimisation thresholds
        - montrer notebook
    - Ajustement groupes et quantité de données - gagne un peu score F1 mais pas autant marqué que learning rate et architecture
        - on suspecte qu'ajouté beaucoup de classes ne scalera pas bien avec le modèle
        - problème avec resources Github
        - mettre screenshot sur ressources bustés (https://github.com/jfgagnon00/FeatheredFury/actions/runs/13033028002 vs https://github.com/jfgagnon00/FeatheredFury/actions/runs/13034156731)

    - tester si ca aide a ne pas mettre de faux positif
        - pas vraiment au final
        - etude sur la classe unkown??

    - Pour présentation finale:
        - on veut piste amelioration pour le produit
        - pour la presentation, on veut une grosse demo technique du produit (le focus est le client)
        - je pense que le prof veut voir son diagramme et ce qui lui correspond dans mon pipeline
        - je pense que l'approche ou on vend la solution pourrait etre bonne pour faire la pres:
            - voici mon flow
            - voici comment vous pourriez l'integrer chez-vous
                - va montrer 
        - les pistes d'améliorations sont importantes aussi

# Semaine du 2 février 2025

- Commencer power point ; sert pas a grand chose de faire un meilleur modele car demande beaucoup de temps

================= Problèmes rencontrés

# Gestion des versions des outils
- dependance des packages python => differents OS (containres, mac, windows)
    - on veut UNE REPRODUCTIBILITE, donc, gerer les versions est important

- outils utilise: 
    - docker et https://docs.docker.com/go/dockerfile/rule/json-args-recommended/


# Keras
- Sequential vs subclassing
- Probleme relie a l'OS 
    # LIMITATION: Il est possible que python lance une erreur 'Too many file open'
    #             Je ne sais pas encore quel est la source du probleme mais un workaround
    #             est de hausser la limite avec 'ulimit -n 2048' ou utiliser le
    #             code python qui suit

    if  platform.system() == "Darwin" :
        import resource
        _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (project_config._ulimit_workaround, hard))
- Support et query GPU

# Securtite et le droit des gens a faire confiance...
- HTTPS
- Azure (infrastructure)
- CORS
- Javascript


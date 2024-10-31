# Tasks
- analyse + preprocess
    - baser sur investigation, preprocess == melspectogram et faire les segments par espece
        - segment seront non overlapper
    - preprocess limite a 10 classes
        - enlever les fichiers trop long
        - enlever les fichiers trop court
        - essaye de detecter le "background" avec un filtre en mediane
            - va servir a valider que les segments contiennent au mois qqch

- train/test/validation split
    - modele inspire de SED: A tutorial
    - mettre configuration et classes wrapper
    - preprocessing (utiliser HDF5 - https://docs.h5py.org/en/stable/)
        - configuration
            - train/validation size en %
            - audio frame size en ms
            - audio window size en ms
            - num mel bands
            - segment size en ms
            - target samplaing rate (reste 22Khz?)
            - pousser sur google drive via dvc
            - wrapper dans command line

- Preparer le training
    - mettre une boucle simple (juste loader data et train 1 epoch)
    - mettre configuration (idee etant d'avoir metriques et logger un moment donne)

- Multiple instance learning
- Data augmentation (si le temps le permet)

# Tasks
- analyse + preprocess
    - finir notebook (done)
    - generer configuration pour split

- train/test/validation split
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

- Trouver modele backbone
    - prendre CNN, semble plus simple pour la suite

- Loader le modele backbone et l'ajuster pour fine-tuning
    - mettre ca en config
    - debuter avec multilayer perceptron pour les dernieres layers

- Preparer le training
    - mettre une boucle simple (juste loader data et train 1 epoch)
    - mettre configuration (idee etant d'avoir metriques et logger un moment donne)

- Few shot learning
- Multiple instance learning
- Data augmentation

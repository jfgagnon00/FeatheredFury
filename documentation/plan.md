# Tasks
- analyse + preprocess
    - baser sur investigation, preprocess == melspectogram et faire les segments par espece
    - split
        - je pense prendre few shot learning pour faire embbeding et trouver les moyennes par classes des embeddings
            - la methode va etre prototypical network avec mediane
            - je vais aussi sortir une variance par classe en plus de la moyenne
            - moyenne + variance va pouvoir me donner un z score ; threshold a determiner
            - toutes ces informations seront appliquees dans le train ; mettre ici pour comptrendre pourquoi ca influence le split

        - few short learning demande de separer train/test/validate en support et query ET ils doivent avoir des classes distinctes. Ex, les classes dans train support NE SONT PAS dans train query ni test ni validation. weird mais c'est ce que j'ai compris

        - comme on travaille avec des segments, faut splitter les segments et non les especes. faut probablement refaire l'analyse exploratoire

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

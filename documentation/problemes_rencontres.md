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


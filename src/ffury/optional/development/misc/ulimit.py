import platform

from ffury.configs import ProjectConfig

def ulimit_workaround(project_config: ProjectConfig) -> None:
    # TODO: a enlever
    # LIMITATION: Il est possible que python lance une erreur 'Too many file open'
    #             Probleme vient de HDF5 et VirtualDataset. Voir https://stackoverflow.com/questions/69941733/h5py-error-reading-virtual-dataset-into-numpy-array
    #             pour details. Il faudrait avoir 1 seul grand fichier pour tous les spectrograms
    if  platform.system() == "Darwin" :
        import resource
        _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (project_config._ulimit_workaround, hard))
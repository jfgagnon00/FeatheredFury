class Logger():
    """
    Encapsule logging (redirection dans fichier, verbosity, etc)
    """

    def __init__(self, verbose):
        self._verbose = verbose

    def log(self, *args, **kwargs):
        if self._verbose:
            print(*args, **kwargs)
    
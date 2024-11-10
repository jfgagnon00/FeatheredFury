def halton_sequence(b):
    """
    Generateur pour sequence Halton.

    Parametre:
        b: base (nombre premier, 2, 3, 11 etc)

    Retour:
        Nombre dans l'interval [0, 1]
    """
    n, d = 0, 1
    while True:
        x = d - n
        if x == 1:
            n = 1
            d *= b
        else:
            y = d // b
            while x <= y:
                y //= b
            n = (b + 1) * y - x
        yield n / d

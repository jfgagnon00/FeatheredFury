def halton_sequence(b, count):
    """
    Generateur pour sequence Halton.

    Parametre:
        b    : base (nombre premier, 2, 3, 11 etc)
        count: Quantite d'elements generes

    Retour:
        Nombre dans l'interval [0, 1]
    """
    n, d = 0, 1
    for _ in range(count):
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

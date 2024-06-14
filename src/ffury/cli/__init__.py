"""
Module encapsulant le commande line.
"""

import click

from .dataset import dataset

@click.group()
def cli():
    pass

def ffury():
    # enregistrer les nouvelles commandes ici
    cli.add_command(dataset)

    # lance le command line
    cli()

if __name__ == '__main__':
    cli()

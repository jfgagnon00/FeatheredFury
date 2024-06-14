import click

@click.command()
@click.option("--force", default=False, is_flag=True, help="Force download")
@click.option("--verbose", default=True, is_flag=True, help="Affiche progression")
@click.argument("path", type=click.Path())
def dataset(force, verbose, path):
    """
    Encapsule installation du dataset venant de Kaggle
    """

    # import du module fait authentication automatiquement
    import kaggle

    # TODO: encapsuler les parametres dans une config
    kaggle.api.competition_download_cli(competition="birdclef-2023",
            # competition_opt=None,
            # file_name=None,
            path=path,
            force=force,
            quiet=not verbose)

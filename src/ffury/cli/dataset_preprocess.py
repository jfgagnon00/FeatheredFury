from pandas import read_csv
from pathlib import Path
from tqdm import tqdm

from . import ProjectConfigDecorator
from .dataset import dataset_group

from ..configs import (
    DatasetType,
    ProjectConfig
)
from ..misc.logging import create_logger
from ..transforms import (
    clean_specie_groups_data,
    copy_specie_groups_data,
    generate_specie_groups,
    generate_species_groups,
    split,
    write_split_sampling_md5
)


@dataset_group.command()
@ProjectConfigDecorator
def preprocess(project_config: ProjectConfig) -> None:
    """
    Resample le dataset en groupes et les split en train/test/validation
    """
    logger = create_logger(file=__file__)

    # cleaner etape precedente
    clean_specie_groups_data(project_config)

    # charger data explore
    filename = project_config.get_csv_filename(DatasetType.EXPLORED)
    logger.info(f"Lecture '{filename}'")
    data_df = read_csv(filename)
    logger.info(f"    {data_df.shape[0]} elements")

    # generer information par espece d'oiseau
    species_groups, species_str, species_categories = generate_species_groups(data_df)

    # ecrire dataset primary_label, common_name dans fichier .csv
    # evite d'avoir des strings partout
    filename = Path(project_config.get_csv_filename(DatasetType._SPECIES))
    logger.info(f"Ecriture '{filename}'")
    filename.parent.mkdir(exist_ok=True, parents=True)
    species_str.to_csv(filename, index=False)

    # resampler le dataset en groupes 
    logger.info(f"Resampling '{filename}'")

    groups_df_filename = Path.joinpath(project_config.paths.BUILD_DIR, "groups.csv")
    groups_df_filename.parent.mkdir(exist_ok=True, parents=True)
    append = False

    for specie_str, specie_infos in tqdm(species_groups):
        # pas besoin du data en tant que tel puisque que des vues seront utilisees
        specie_groups_df = generate_specie_groups(specie_infos,
                                                  species_categories.get_loc(specie_str),
                                                  project_config.preprocess)

        copy_specie_groups_data(specie_groups_df,
                                project_config)

        specie_groups_df.to_csv(groups_df_filename, 
                                mode="a" if append else "w", 
                                index=False, 
                                header=not append)
        append = True

    logger.info(f"Split")
    train_df, test_df, validation_df = split(read_csv(groups_df_filename), 
                                                      project_config.preprocess)
    
    train_df.to_csv(project_config.get_csv_filename(DatasetType.TRAIN), 
                    mode="w", 
                    index=False)
    
    test_df.to_csv(project_config.get_csv_filename(DatasetType.TEST), 
                   mode="w", 
                   index=False)
    
    validation_df.to_csv(project_config.get_csv_filename(DatasetType.VALIDATION), 
                         mode="w", 
                         index=False)

    # prendre en note une signature des parametres utilises pour le preprocessing
    logger.info(f"Ecriture signature md5")
    write_split_sampling_md5(project_config)

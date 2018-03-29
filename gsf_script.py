
from zipfile import ZipFile
from shutil import move, copy
import csv
import logging.config

import constants

from engine import get_type
from utils import check_file, validation_yes_no, get_config
from livraison_tibco_ear import livraison_ear
from transform_ear_profile import moulinette_profile
from livraison_tibco_ems import livraison_ems
from transform_ems_script import moulinette_ems
from livraison_net import livraison_net
from livraison_sql import livraison_sql


def arg_parser():
    # Creation du parser
    parser = argparse.ArgumentParser(
        description='Script permettant de livrer les éléments tibco',
        epilog='Made with <3 !'
    )

    # Arguments facultatifs
    parser.add_argument('-d', '--delimiter', default=';', help='the delimiter in the csv file default ";"')

    # Groupe pour les args obligatoires
    required = parser.add_argument_group('required arguments')

    required.add_argument('-csv', '--csv', help='le csv contenant la description de la livraison', required=True)
    required.add_argument('-env', '--environment', help='L\'environnement cible',
                          choices=constants.LIST_ENV,
                          required=True)

    # Parse les arguments
    return parser.parse_args()

if __name__ == '__main__':
    LOGGING_CONF = get_config('LOGGING_CONF')
    EMS_MATRICE_PATH = get_config('EMS_MATRICE_PATH')
    DEPOT_MATRICE = get_config('DEPOT_MATRICE')
    EMS_MATRICE_PATH = get_config('EMS_MATRICE_PATH')
    PROFILE_MATRICE_PATH = get_config('PROFILE_MATRICE_PATH')
    TYPE_FILE_PATH = get_config('TYPE_FILE_PATH')
    DEPOT = get_config('DEPOT')
    EXTRACT_PATH = get_config('EXTRACT_PATH')

    logging.config.fileConfig(LOGGING_CONF)
    logger = logging.getLogger(constants.LOGGER)
    logger.info('Lancement de la livraison')
    args = arg_parser()
    # Copie des matrices
    logger.info('Copie des matrices :')
    logger.info('Copie de la matrice EMS')
    logger.debug('from {} to {}'.format(EMS_MATRICE_PATH, DEPOT_MATRICE))
    matrice_ems = copy(EMS_MATRICE_PATH, DEPOT_MATRICE)
    logger.info('Copie de la matrice terminée')
    logger.info('Copie de la matrice profile')
    logger.debug('from {} to {}'.format(PROFILE_MATRICE_PATH, DEPOT_MATRICE))
    matrice_profile = copy(PROFILE_MATRICE_PATH, DEPOT_MATRICE)
    logger.info('Copie de la matrice terminée')
    logger.info('Copie de la matrice type')
    logger.debug('from {} to {}'.format(TYPE_FILE_PATH, DEPOT_MATRICE))
    matrice_type = copy(TYPE_FILE_PATH, DEPOT_MATRICE)
    logger.info('Copie de la matrice terminée')
    logger.info('Copie de la matrice BL')
    logger.debug('from {} to {}'.format(args.csv, DEPOT_MATRICE))
    BL = copy(args.csv, DEPOT_MATRICE)
    logger.info('Copie de la matrice terminée')
    dict_type = get_type(matrice_type,
                         args.delimiter,
                         args.environment)
    try:
        check_file(BL, ('.csv', '.CSV'))
        with open(BL, 'r') as csv_list_liv:
            reader = csv.DictReader(csv_list_liv, delimiter=args.delimiter)
            for row in reader:
                if row[constants.BL_TYPE] in dict_type.keys():
                    elem = row[constants.BL_TYPE].split('-', 1)[0]
                    if elem == constants.TYPE_EAR:
                        logger.info('Livraison ear')
                        # Copy from NAS
                        logger.info('Recuperation de l\'ear')
                        ear_origin = row[constants.BL_PATH_NAS]+'\\'+row[constants.BL_LIVRABLE]
                        logger.debug('Copie de {} à {}'.format(ear_origin, DEPOT))
                        ear_path = copy(ear_origin, DEPOT)
                        logger.info('Recuperation de l\'ear OK')
                        # Extract profile
                        with ZipFile(ear_path) as ear_zip:
                            logger.info('Extraction du profile')
                            logger.debug('Extraction vers : {}'.format(EXTRACT_PATH))
                            extracted = ear_zip.extract(constants.PROFILE_PATH_IN_EAR, EXTRACT_PATH)
                            logger.info('Extraction OK : {}'.format(extracted))
                            # Rename profile
                            logger.info('Rennomage du profil')
                            profile_path = DEPOT+'\\'+row[constants.BL_LIVRABLE]+'.substvar'
                            move(extracted, profile_path)
                            logger.debug('Profile : {}'.format(profile_path))
                            logger.info('rennomage ok')
                        # Transformation
                        logger.info('Transformation du profil')
                        transformed_profile = DEPOT + '\\'+args.environment+'_' + row[constants.BL_LIVRABLE] +'.substvar'
                        moulinette_profile(
                            matrice_profile,
                            args.environment,
                            args.delimiter,
                            profile_path,
                            transformed_profile
                        )
                        logger.info('transformation du profile OK')
                        # Domain et appspace
                        type_info = dict_type[row[constants.BL_TYPE]].split()
                        domain = type_info[0]
                        appspace = type_info[1]
                        logger.info('Livraison EAR')
                        # Livraison
                        livraison_ear(
                            ear_path,
                            domain,
                            appspace,
                            transformed_profile,
                            replace=validation_yes_no('Replace ear pendant le deploy ?')
                        )
                        logger.info('livraison OK')
                    elif elem == constants.TYPE_EMS:
                        # Copy from NAS
                        logger.info('Livraison EMS')
                        logger.info('Copie depuis le NAS')
                        ems_path = copy(row[constants.BL_PATH_NAS]+'\\'+row[constants.BL_LIVRABLE], DEPOT)
                        logger.debug(ems_path)
                        # transformation
                        logger.info('Transformation')
                        transformed_ems = DEPOT + '\\'+args.environment+'_' + row[constants.BL_LIVRABLE]
                        logger.debug(transformed_ems)
                        moulinette_ems(
                            matrice_ems,
                            args.environment,
                            args.delimiter,
                            ems_path,
                            transformed_ems
                        )
                        logger.info('Livraison')
                        # Server user password
                        type_info = dict_type[row[constants.BL_TYPE]].split()
                        logger.debug(type_info)
                        server = type_info[0]
                        user = type_info[1]
                        password = type_info[2]
                        # TODO: trouver solution plus elegante
                        # Utilisé pour les mdp vide
                        if password == '\'\'':
                            password = ''
                        # Livraison
                        livraison_ems(
                            transformed_ems,
                            server,
                            user,
                            password
                        )
                    elif elem == constants.TYPE_NET:
                        logger.info('Livraison NET')
                        app_path = dict_type[row[constants.BL_TYPE]]
                        app_source = row[constants.BL_PATH_NAS]
                        livraison_net(app_source, app_path)
                    elif elem == constants.TYPE_SQL:
                        # set NLS_LANG
                        script_path = row[constants.BL_PATH_NAS] + '\\' + row[constants.BL_LIVRABLE]
                        url = dict_type[row[constants.BL_TYPE]].split()
                        logger.debug('script_path : {}'.format(script_path))
                        logger.debug('url : {}'.format(url))
                        livraison_sql(script_path, DEPOT, url)
                    else:
                        logger.warning('Automatisation indisponible pour : {} -> {}'
                                       .format(row[constants.BL_TYPE], row[constants.BL_LIVRABLE]))
                else:
                    print('Unknown type : {} : {}'.format(row[constants.BL_TYPE], row[constants.BL_LIVRABLE]))
    except FileNotFoundError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


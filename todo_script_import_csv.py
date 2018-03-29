# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

import configparser
import argparse
import sys
from pprint import pprint
import logging
import logging.config

import csv



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="préciser le fichier de configuration")
    parser.add_argument("csvfile", help="préciser le nom du fichier à importer")
    args = parser.parse_args()
    config_ini = configparser.ConfigParser()
    config_ini.read(args.config)
    
    logging.config.fileConfig(config_ini['LOG']['logconfig'])    
    logger = logging.getLogger('root')

    with open(args.csvfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=";")
        for row in reader:
            print(row)

    
    sys.exit(1)
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

    config = {
        'user': config_ini['DATABASE']['login'],
        'password': config_ini['DATABASE']['password'],
        'host': config_ini['DATABASE']['host'],
        'database': config_ini['DATABASE']['database'],
        'port':config_ini['DATABASE']['port']
    }
    cnx = cur = None

    logging.config.fileConfig(config_ini['LOG']['logconfig'])    
    logger = logging.getLogger('root')
    try:
        cnx = mysql.connector.connect(**config)
        cur = cnx.cursor()
        query = "INSERT INTO todos(action, dueDate) VALUES(%s,%s)"
        with open(args.csvfile, newline='') as csvfile:
            reader = csv.DictReader(csvfile,delimiter=";")

            for row in reader:
                data = (row['action'],row['dueDate'])
                cur.execute(query,data)
        
        cnx.commit()
    except:
        print("erreur !")
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
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S',  level=logging.DEBUG)
    


    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="préciser le fichier de configuration")
    args = parser.parse_args()    
    config_ini = configparser.ConfigParser()
    config_ini.read(args.config)
    
    logging.config.fileConfig(config_ini['LOG']['logconfig'])    
    logger = logging.getLogger('root')

    config = {
        'user': config_ini['DATABASE']['login'],
        'password': config_ini['DATABASE']['password'],
        'host': config_ini['DATABASE']['host'],
        'database': config_ini['DATABASE']['database'],
        'port':config_ini['DATABASE']['port']
    }

    cnx = cur = None
    try:
        logger.debug('db connection.')
        cnx = mysql.connector.connect(**config)
        cur = cnx.cursor()
        query = "SELECT id,action,dueDate FROM todos;"
        cur.execute(query)
        with open('todos.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'action','dueDate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=";")
            writer.writeheader()
            for id,action,dueDate in cur.fetchall():               
                
                writer.writerow(
                        {
                            'id': id, 
                            'action': action,
                            'dueDate':dueDate
                        })

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    finally:
        if cur:
            cur.close()
        if cnx:
            cnx.close()
    
    sys.exit(1)            
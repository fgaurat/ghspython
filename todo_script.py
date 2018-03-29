# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

import configparser
import argparse
import sys
from pprint import pprint


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="préciser le fichier de configuration")
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
    try:
        cnx = mysql.connector.connect(**config)
        cur = cnx.cursor()
        query = "SELECT id,action,dueDate FROM todos;"
        cur.execute(query)
        
        for id,action,dueDate in cur.fetchall():
            print(action)
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
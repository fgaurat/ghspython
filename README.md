https://pip.pypa.io/en/stable/installing/

https://pypi.python.org/pypi

# -*- coding: utf-8 -*-

https://docs.python.org/3/tutorial/introduction.html



https://www.jetbrains.com/pycharm/

https://docs.python.org/3/tutorial/modules.html

Windows 7 :
https://docs.docker.com/toolbox/toolbox_install_windows/

Windows 10 :
https://store.docker.com/editions/community/docker-ce-desktop-windows

DBeaver
https://dbeaver.jkiss.org/download/

---------------------------------------------------------------------------
CREATE TABLE tododb.todos (
	id INT NOT NULL AUTO_INCREMENT,
	`action` varchar(100) NULL,
	dueDate varchar(100) NULL,
	CONSTRAINT todos_PK PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci ;

---------------------------------------------------------------------------


INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 1', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 2', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 3', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 1', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 2', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 3', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 1', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 2', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 3', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 1', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 2', '1522245898');
INSERT INTO tododb.todos(`action`, dueDate) VALUES('Action 3', '1522245898');


---------------------------------------------------------------------------

pip install mysql-connector

---------------------------------------------------------------------------

https://github.com/sanpingz/mysql-connector

---------------------------------------------------------------------------

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
    config = configparser.ConfigParser()
    config.read(args.config)
        
    config = {
        'user': config['DATABASE']['login'],
        'password': config['DATABASE']['password'],
        'host': config['DATABASE']['host'],
        'database': config['DATABASE']['database'],
        'port':config['DATABASE']['port']
    }

    cnx = cur = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur = cnx.cursor()
        cur.execute('show databases;')
        
        for row in cur.fetchall():
            print(row)


    finally:
        if cur:
            cur.close()
        if cnx:
            cnx.close()
    
    sys.exit(1)            


---------------------------------------------------------------------------


https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html



https://docs.python.org/3/howto/logging.html#logging-basic-tutorial



https://docs.python.org/3/library/csv.html
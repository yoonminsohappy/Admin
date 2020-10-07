import pymysql

from config import database

def get_connection():
    return pymysql.connect(
        host       = database['host'],
        port       = database['port'],
        user       = database['user'],
        passwd     = database['password'],
        db         = database['database'],
        charset    = 'utf8mb4',
        autocommit = False
)
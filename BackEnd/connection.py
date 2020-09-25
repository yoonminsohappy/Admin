import pymysql

def get_connection(db):
    return pymysql.connect(
        host       = db['host'],
        port       = db['port'],
        user       = db['user'],
        passwd     = db['password'],
        db         = db['database'],
        charset    = 'utf8mb4',
        autocommit = False
    )

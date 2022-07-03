import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host= 'database-2.c05d0e8qcds2.sa-east-1.rds.amazonaws.com',
        port = 3306,
        user ='admin',
        password ='projeto2',
        cursorclass=pymysql.cursors.DictCursor,
        db='sys'
    )


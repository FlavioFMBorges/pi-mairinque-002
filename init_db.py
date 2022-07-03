import pymysql
import pymysql.cursors
import os
def get_db_connection():
    return pymysql.connect(
        host= os.environ['HOST'],
        port = 3306,
        user = os.environ['USER'],
        password = os.environ['PASSWORD'],
        cursorclass=pymysql.cursors.DictCursor,
        db='sys'
    )

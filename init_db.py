import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host= HOST,
        port = 3306,
        user = USER,
        password = PASSWORD,
        cursorclass=pymysql.cursors.DictCursor,
        db='sys'
    )

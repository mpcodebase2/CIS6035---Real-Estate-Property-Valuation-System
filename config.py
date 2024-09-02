import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'P347word@$#'
    MYSQL_DB = 'user_auth'
    MYSQL_CURSORCLASS = 'DictCursor'

from peewee import CharField, Model, MySQLDatabase
from app import app

MYSQL_DB = 'users'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = 'root'

db = MySQLDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class tbl_users2(BaseModel):
    user_name = CharField(primary_key=True)
    user_password = CharField()

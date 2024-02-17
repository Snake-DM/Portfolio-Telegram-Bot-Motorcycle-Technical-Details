import datetime
import os
from peewee import *
from loguru import logger


@logger.catch
def db_create() -> SqliteDatabase:
    """
    Function creates a database file
    :return: SqliteDatabase
    """
    work_directory = os.path.abspath(os.getcwd())
    db_abspath = os.path.join(work_directory, 'database', 'participants.db')
    if os.path.isfile(db_abspath):
        print("A database exists already and it will continue logging.")
    else:
        print('New database has been created successfully.')
    new_db = SqliteDatabase(db_abspath)
    return new_db


main_db = db_create()


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = main_db
        order_by = 'created_at'


class UserData(BaseModel):
    created_at = DateTimeField(default=datetime.datetime.now().isoformat(
                               sep=' ', timespec='seconds'))
                               # strftime("%Y-%m-%d %H:%M:%S"))
    from_user_id = IntegerField()
    nickname = CharField(null=True)
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    age = CharField(null=True)
    moto_experience = CharField(null=True)

    class Meta:
        db_table = 'Active Users'


class UserMessageLog(BaseModel):
    created_at = DateTimeField(default=datetime.datetime.now().isoformat(
                               sep=' ', timespec='seconds'))
                               # strftime("%Y-%m-%d %H:%M:%S"))
    from_user_id = ForeignKeyField(UserData)
    user_message = CharField()

    class Meta:
        db_table = 'Message Log for a User'


main_db.create_tables([UserData, UserMessageLog])

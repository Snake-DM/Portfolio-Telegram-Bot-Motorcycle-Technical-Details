import os
from peewee import *
from loguru import logger


work_directory = os.path.abspath(os.getcwd())
db_abspath = os.path.join(work_directory, 'database', 'participants.db')
if os.path.isfile(db_abspath):
    main_db = SqliteDatabase('database/participants.db')
    print('Database exists already')
else:
    try:
        main_db = SqliteDatabase('database/participants.db')
        print('New database has been created successfully')
    except Exception as err:
        print('Error: ', err)
        logger.debug('Error')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = main_db
        order_by = 'id'


class UserData(BaseModel):
    from_user_id = CharField()
    name = CharField(null=True)
    age = CharField(null=True)
    moto_experience = CharField(null=True)

    class Meta:
        db_table = 'Active Users'


class UserMessageLog(BaseModel):
    from_user_id = ForeignKeyField(UserData)
    user_message = CharField()

    class Meta:
        db_table = 'Message Log for a User'


with main_db:
    main_db.create_tables([UserData, UserMessageLog])

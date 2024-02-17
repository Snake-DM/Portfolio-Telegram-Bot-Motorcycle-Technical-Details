from database import database
from peewee import *


class DatabaseCustomCRUD:
    """
    Class performs a basic actions with an active database:
        - new user check
        - log a user data like age, motorcycle driving experience
        - log a message from a user
        - TBD
    """

    def __init__(self, active_db: SqliteDatabase) -> None:
        """
        Class initiation
        :param active_db: SqliteDatabase
        """
        pass

    @staticmethod
    def new_user_check(user_id: int) -> bool:
        """
        Method checks whether a new user has been registered in database
        already.
        :param user_id: int
        :return: bool
        """
        # with self.active_db as data:
        if database.UserData.get_or_none(from_user_id=user_id):
            return True
        else:
            return False

    @staticmethod
    def log_user(user_id: int,
                 u_nickname: str = None,
                 u_firstname: str = None,
                 u_lastname: str = None,
                 u_age: str = None,
                 u_moto_exp: str = None) -> None:
        """
        A method logs user's name, age, moto experience into a database table
        UserData

        :param user_id: from_user.id object from pyTelegramBotAPI
        :param u_nickname: str
        :param u_firstname: str
        :param u_lastname: str
        :param u_age: str
        :param u_moto_exp: str
        :return: none
        """

        if not (u_nickname or
                u_firstname or
                u_lastname or
                u_age or
                u_moto_exp):
            database.UserData.create(
                from_user_id=user_id)
        else:
            (database.UserData.update(
                nickname=u_nickname,
                firstname=u_firstname,
                lastname=u_lastname,
                age=u_age,
                moto_experience=u_moto_exp)
             .where(database.UserData.from_user_id == user_id)
             .execute())

    @staticmethod
    def log_message(user_id: int,
                    message: str) -> None:
        """
        A method logs user's messages into the database table UserMessageLog

        :param user_id: from_user.id object from pyTelegramBotApi
        :param message: str
        :return: none
        """

        database.UserMessageLog.create(
            from_user_id=user_id,
            user_message=message,
        )


db_customCRUD = DatabaseCustomCRUD(database.main_db)

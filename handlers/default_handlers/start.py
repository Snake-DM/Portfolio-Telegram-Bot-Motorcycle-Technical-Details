from telebot.types import Message

from loader import bot
from states.contact_info import UserInfoState
from database import database
import os.path


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
   Function requests a new username.
   :param message: incoming message from a user
   :return: None
   """

    if database.UserData.get_or_none(from_user_id=message.from_user.id):
        bot.send_message(message.from_user.id,
                         'Бот уже запущен. Воспользуйтесь другой командой.')
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id,
                         f'Здравствуйте, {message.from_user.username}!\n'
                         f'Данный бот позволит Вам найти детальную справочную '
                         f'информацию по различным моделям мотоциклов.')

        # with database.main_db:
        database.UserData.create(
                from_user_id=message.from_user.id)

        # history log update
        database.UserMessageLog.create(
                from_user_id=message.from_user.id,
                user_message=message.text,
        )

        bot.set_state(message.from_user.id, UserInfoState.name,
                      message.chat.id)
        bot.send_message(message.from_user.id, f'\nВведите своё имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    """
    Function register a user's name and requests an age
    :param message: incoming message from a user
    :return: None
    """
    if message.text.isalpha():
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['from_user_id'] = message.from_user.id
            data['name'] = message.text

        bot.send_message(message.from_user.id, 'Введите свой возраст, лет')

        # history log update
        database.UserMessageLog.create(
                from_user_id=message.from_user.id,
                user_message=message.text,
        )

    else:
        bot.send_message(message.from_user.id,
                         'Имя может содержать только буквы.'
                         'Попробуйте ещё раз')


@bot.message_handler(state=UserInfoState.age, is_digit=True)
def get_age(message: Message) -> None:
    """
    Function registers the Age and requests a motorcycle experience
    :param message: incoming message from a user
    :return: None
    """
    bot.set_state(message.from_user.id,
                  UserInfoState.moto_driving_experience, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

    bot.send_message(message.from_user.id, 'Введите свой опыт вождения '
                                           'мотоцикла, лет')


@bot.message_handler(state=UserInfoState.age, is_digit=False)
def get_age_wrong(message: Message) -> None:
    """
    Function filters an Age wrong input
    :param message: incoming message from a user
    :return: None
    """
    bot.send_message(message.from_user.id,
                     'Возраст может содержать только цифры. Попробуйте '
                     'ещё раз')


@bot.message_handler(state=UserInfoState.moto_driving_experience,
                     is_digit=True)
def get_moto_experience(message: Message) -> None:
    """
    Function registers motorcycle experience and publish a user summary data
    :param message: incoming message from a user
    :return: None
    """
    bot.send_message(message.from_user.id, 'Благодарю')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['moto_experience'] = message.text

    msg = ("Ваши данные:\n"
           f"Имя: {data['name']}\n"
           f"Возраст, лет: {data['age']}\n"
           f"Опыт вождения мотоцикла, лет:"
           f" {data['moto_experience']}\n")
    bot.send_message(message.chat.id, msg)

    # DB Update
    # (with database.main_db):
    database.UserData.update(
            name=data['name'],
            age=data['age'],
            moto_experience=data['moto_experience']
    ).where(
            database.UserData.from_user_id ==
            message.from_user.id
    ).execute()

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

    msg = (f"{data['name']}!\n"
           f"Выберите параметры поиска мотоциклов через команды.\n"
           f"Для начала используйте команду /help.")
    bot.send_message(message.chat.id, msg)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=UserInfoState.moto_driving_experience,
                     is_digit=False)
def get_moto_experience(message: Message) -> None:
    """
    Function filters a motorcycle experience wrong input
    :param message: incoming message from a user
    :return: None
    """
    bot.send_message(message.from_user.id, 'Опыт вождения может '
                                           'содержать только цифры. '
                                           'Попробуйте ещё раз.')

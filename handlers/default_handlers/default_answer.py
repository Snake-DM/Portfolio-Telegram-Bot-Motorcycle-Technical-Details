from telebot.types import Message
from database.db_crud import db_customCRUD
from loader import bot
from states.contact_info import UserInfoState


@bot.message_handler(state=None)
def default_answer(message: Message) -> None:
    """
    A default handler to reply a user which send an unknown
    command or text.

    :param message: incoming message from a user
    :return: none
    """
    bot.send_message(message.chat.id, "Не понимаю Вас: \"" + message.text +
                     "\".\nПопробуйте получить помощь, введя команду /help")

    # history log update
    db_customCRUD.log_message(message.from_user.id, message.text)
#
# NOTE:  for future reference:
#
# @bot.message_handler(state=None)
# def default_answer(message: Message) -> None:
#     """
#     A default handler unregistered user asking to proceed with a command
#     /start.
#
#     :param message: incoming message from a user
#     :return: none
#     """
#     bot.send_message(message.chat.id,
#                      'Здравствутйе. Вы здесь впервые. Пожалуйста, начните '
#                      'использование бота с команды "/Start" чтобы пройти '
#                      'процедуру регистрации.')
#
#     # history log update
#     db_customCRUD.log_message(message.from_user.id, message.text)

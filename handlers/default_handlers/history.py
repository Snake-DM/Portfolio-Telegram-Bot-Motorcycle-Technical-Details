from telebot.types import Message

from database import database
from database.db_crud import db_customCRUD
from loader import bot


@bot.message_handler(commands=['history'])
def print_history(message: Message) -> None:
    """
    This handler sends a message with a user's input History (10 last
    messages to Bot)
    :param message: incoming message from a user
    :return: none
    """
    # getting a chat history from DB
    bot.send_message(message.from_user.id,
                     'Ваша история запросов (последние 10 записей):')
    user_messages = (
        database.
        UserMessageLog.
        select().
        where(database.UserMessageLog.from_user_id == message.from_user.id)
        )
    user_history_message_list = [message.user_message for message in
                                 user_messages]

    history_reply = '\n'.join(user_history_message_list[-10:])
    bot.send_message(message.from_user.id, history_reply)

    # history log update
    db_customCRUD.log_message(message.from_user.id, message.text)

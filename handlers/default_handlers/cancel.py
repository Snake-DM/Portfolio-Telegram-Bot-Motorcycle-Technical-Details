from telebot.types import Message

from database.db_crud import db_customCRUD
from loader import bot


@bot.message_handler(state="*", commands=["cancel"])
def cancel_state(message: Message) -> None:
    """
    Function cancels any command for the current User.
    :param message: incoming message from a user
    :return: none
    """
    bot.reply_to(message, f"Команда отменена. Введите новую команду или "
                          f"воспользуйтесь помощью c /help")
    bot.delete_state(message.from_user.id, message.chat.id)

    # history log update
    db_customCRUD.log_message(message.from_user.id, message.text)

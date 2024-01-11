from telebot.types import Message

from database import database
from loader import bot



@bot.message_handler(state=None)
def default_answer(message: Message) -> None:
    """
    A default handler for every other text. This is the standard reply to
    unknown message

    :param message: incoming message from a user
    :return: none
    """
    bot.send_message(message.chat.id, "Не понимаю Вас: \"" + message.text +
                     "\".\nПопробуйте получить помощь, введя команду /help")

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

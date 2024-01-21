from telebot.types import Message
from loader import bot

# TODO who to make it work in any state?


@bot.message_handler(commands=["cancel"], state=not None)
def bot_stop(message: Message) -> None:
    """
    Function cancels any command for the current User.
    :param message: incoming message from a user
    :return: none
    """
    bot.reply_to(message, f"Команда отменена. Введите новую команду или "
                          f"воспользуйтесь помощью c /help")
    bot.delete_state(message.from_user.id, message.chat.id)

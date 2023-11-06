from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["history"])
def history(message: Message):
    bot.send_message(message.from_user.id,
                     'Здесь будет выводиться история запросов пользователя')

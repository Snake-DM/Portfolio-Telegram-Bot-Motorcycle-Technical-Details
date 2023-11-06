from telebot.types import Message
from loader import bot


# default handler for every other text
# this is the standard reply to unknown message

@bot.message_handler(state=None)
def default_answer(message: Message):
    bot.send_message(message.chat.id, "Не понимаю Вас: \"" + message.text +
                     "\".\nПопробуйте получить помощь, введя команду /help")

from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["stop"])
def bot_stop(message: Message) -> None:
    bot.reply_to(message, f"До свидания, {message.from_user.full_name}!")
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.stop_bot()

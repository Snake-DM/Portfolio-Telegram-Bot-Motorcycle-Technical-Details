from telebot.types import Message
from loader import bot


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message) -> None:
#     bot.send_message(message.chat.id, message.text)


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )

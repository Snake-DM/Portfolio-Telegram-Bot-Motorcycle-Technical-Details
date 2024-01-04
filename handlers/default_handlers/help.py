from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from database import database
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {description}" for command, description in
            DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

from telebot.types import Message

from database import database
from loader import bot


@bot.message_handler(commands=["stop"])
def bot_stop(message: Message) -> None:
    bot.reply_to(message, f"До свидания, {message.from_user.full_name}!")
    bot.delete_state(message.from_user.id, message.chat.id)

    person = database.UserData.get(database.UserData.from_user_id ==
                                   message.from_user.id)
    person.delete_instance()

    bot.stop_bot()


#
# inactive_users = User.select().where(User.active == False)
#
# # Here, instead of defaulting to all columns, Peewee will default
# # to only selecting the primary key.
# Tweet.delete().where(Tweet.user.in_(inactive_users)).execute()

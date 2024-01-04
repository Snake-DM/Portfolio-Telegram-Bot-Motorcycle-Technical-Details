from telebot.types import Message

from database import database
from loader import bot
from states.search_states import SearchStates


# history handler to save messages for a user
# @bot.message_handler(state=None)
# def saving_user_history(message: Message):
#     # DB Update with user's messages
#     # (with database.main_db:)
#
#     if database.UserData.get_or_none(from_user_id=message.from_user.id):
#         database.UserMessageLog.create(
#                 from_user_id=message.from_user.id,
#                 command=message.text,
#                 request=''
#     )


@bot.message_handler(commands=['history'])
def print_history(message: Message):
    # getting a chat history from DB
    bot.send_message(message.from_user.id, 'Ваша история запросов:')
    user_messages = database.UserMessageLog.select().where(
            database.UserMessageLog.from_user_id ==
            message.from_user.id)
    user_history_message_list = [message.user_message for message in
                              user_messages]

    history_reply = '\n'.join(user_history_message_list[-10:])
    bot.send_message(message.from_user.id, history_reply)

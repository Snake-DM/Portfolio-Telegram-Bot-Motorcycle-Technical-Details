from telebot.types import Message

from database import database
from loader import bot
from custom_requests.api_request import api_request
from states.search_states import SearchStates
from utils.message_max_length_validation import message_max_length
import json


@bot.message_handler(state=SearchStates.brand_year_no)
def brand_year_no(message: Message) -> None:
    """
    Function registers a Year parameter (yes/no) and proceeds with option
    "No" in current state.
    Option "Yes" changes state.

    :param message: incoming message from a user
    :return: none
    """

    if message.text.lower() == "да":
        bot.set_state(message.from_user.id,
                      SearchStates.brand_year_yes,
                      message.chat.id)
        bot.send_message(message.from_user.id, 'Какой год выпуска?')

    elif message.text.lower() == "нет":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            answer = api_request("/v1/motorcycles",
                                 {'make': data['brand']},
                                 "GET")
        if not answer:
            bot.send_message(message.from_user.id, 'Такой брэнд не найден в '
                                                   'базе. Попробуйте '
                                                   'ввести другой '
                                                   'вариант.')
            bot.set_state(message.from_user.id,
                          SearchStates.brand,
                          message.chat.id)
        else:
            answer = json.dumps(answer, indent=4)
            # Answer is split into several messages
            while answer:
                # valid length message
                bot.send_message(message.from_user.id,
                                 message_max_length(answer)[0])
                # tail message
                answer = message_max_length(answer)[1]
            bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Введите Да или Нет.')

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

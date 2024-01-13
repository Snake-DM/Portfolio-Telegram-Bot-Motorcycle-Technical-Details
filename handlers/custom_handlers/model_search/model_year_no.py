import json

from telebot.types import Message

from database import database
from loader import bot
from states.search_states import SearchStates
from custom_requests.api_request import api_request
from utils.message_max_length_validation import message_max_length


@bot.message_handler(state=SearchStates.model_year_no)
def model_year_no(message: Message) -> None:
    """
    Function registers a Year parameter (yes/no) and proceeds with option
    "No" in current state.
    Option "Yes" changes state.

    :param message: incoming message from a user
    :return: none
    """
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id,
                      SearchStates.model_year_yes,
                      message.chat.id)
        bot.send_message(message.from_user.id, 'Какой год выпуска?')
    elif message.text.lower() == 'нет':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            answer = api_request("/v1/motorcycles",
                                 {'model': data['model']},
                                 "GET")
        if not answer:
            bot.send_message(message.from_user.id, 'Такая модель не найдена в '
                                                   'базе. Попробуйте '
                                                   'ввести другую '
                                                   'модель.')
            bot.set_state(message.from_user.id,
                          SearchStates.model,
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

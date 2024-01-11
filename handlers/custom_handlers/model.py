import json

from telebot.types import Message

from database import database
from loader import bot
from states.search_states import SearchStates
from custom_requests.api_request import api_request
from utils.message_max_length_validation import message_max_length


@bot.message_handler(commands=["model"])
def model_query(message: Message) -> None:
    """
    This handler starts a search by Model.

    :param message: incoming message from a user
    :return: none
    """
    bot.set_state(message.from_user.id, SearchStates.model, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название модели, '
                                           f'которую Вы ищете.')

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

@bot.message_handler(state=SearchStates.model)
def get_model(message: Message) -> None:
    """
    Function receives a Model name, requests a Year parameter (yes/no) and
    redirects to appropriate function

    :param message: incoming message from a user
    :return: none
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['model'] = message.text
    bot.send_message(message.from_user.id, 'Желаете указать год выпуска? '
                                           '(да/нет)')
    bot.register_next_step_handler(message, get_model_year)

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )


def get_model_year(message: Message) -> None:
    """
    Function redirects to other function based on Year
    parameter (yes/no)

    :param message: incoming message from a user
    :return: none
    """
    if message.text == 'да':
        bot.send_message(message.from_user.id, 'Какой год выпуска?')
        bot.register_next_step_handler(message, get_model_year_yes)
    elif message.text == 'нет':
        get_model_year_no(message)
    else:
        bot.send_message(message.from_user.id, 'Введите Да или Нет.')
        bot.register_next_step_handler(message, get_model_year)

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )


def get_model_year_yes(message: Message):
    """
    Function extracts data with Year parameter "Yes".

    :param message: incoming message from a user
    :return: none
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['year'] = message.text
    answer = api_request("/v1/motorcycles",
                         {'model': data['model'],
                          'year':  data['year']},
                         "GET")
    if not answer:
        bot.send_message(message.from_user.id, 'Такая модель не найдена в '
                                               'базе. Попробуйте '
                                               'ввести другой '
                                               'год выпуска.')
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

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )


def get_model_year_no(message: Message) -> None:
    """
    Function extracts data with Year parameter "No".

    :param message: incoming message from a user
    :return: none
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        pass
    answer = api_request("/v1/motorcycles",
                         {'model': data['model']},
                         "GET")
    if not answer:
        bot.send_message(message.from_user.id, 'Такая модель не найдена в '
                                               'базе. Попробуйте '
                                               'ввести другую '
                                               'модель.')
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

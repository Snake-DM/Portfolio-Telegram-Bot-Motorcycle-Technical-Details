from telebot.types import Message
from loader import bot
from custom_requests.api_request import api_request
from states.search_states import SearchStates
from utils.message_max_length_validation import message_max_length
import json


@bot.message_handler(commands=["brand"])
def brand_query(message: Message) -> None:
    bot.set_state(message.from_user.id, SearchStates.brand, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название брэнда, '
                                           f'который Вы ищете.')


@bot.message_handler(state=SearchStates.brand)
def get_brand(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['brand'] = message.text
    bot.send_message(message.from_user.id, 'Желаете указать год выпуска? '
                                           '(да/нет)')
    bot.register_next_step_handler(message, get_brand_year)


def get_brand_year(message: Message):
    if message.text == 'да':
        bot.send_message(message.from_user.id, 'Какой год выпуска?')
        bot.register_next_step_handler(message, get_brand_year_yes)
    elif message.text == 'нет':
        get_brand_year_no(message)
    else:
        bot.send_message(message.from_user.id, 'Введите Да или Нет.')
        bot.register_next_step_handler(message, get_brand_year)


def get_brand_year_yes(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['year'] = message.text
    answer = api_request("/v1/motorcycles",
                         {'make': data['brand'],
                          'year':  data['year']},
                         "GET")
    if not answer:
        bot.send_message(message.from_user.id, 'Такой брэнд не найден в '
                                               'базе. Попробуйте '
                                               'ввести другой '
                                               'год выпуска.')
        bot.register_next_step_handler(message, get_brand_year_yes)
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


def get_brand_year_no(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        pass
    answer = api_request("/v1/motorcycles",
                         {'make': data['brand']},
                         "GET")
    if not answer:
        bot.send_message(message.from_user.id, 'Такой брэнд не найден в '
                                               'базе. Попробуйте '
                                               'ввести другой '
                                               'вариант.')
        bot.register_next_step_handler(message, get_brand_year_no)
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

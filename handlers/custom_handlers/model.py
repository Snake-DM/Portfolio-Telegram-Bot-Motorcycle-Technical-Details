from telebot.types import Message
from loader import bot
from custom_requests.api_request import api_request
from states.search_states import SearchStates
from utils.message_max_length_validation import message_max_length
import json


@bot.message_handler(commands=["model"])
def model_query(message: Message) -> None:
    bot.set_state(message.from_user.id, SearchStates.model, message.chat.id)
    print(bot.get_state(message.from_user.id))
    bot.send_message(message.from_user.id, f'Введите название модели, '
                                           f'которую Вы ищете.')


@bot.message_handler(state=SearchStates.model)
def get_model(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Благодарю')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['model'] = message.text
    answer = api_request("/v1/motorcycles",
                         {"model": data['model']},
                         "GET")

    if not answer:
        bot.send_message(message.from_user.id, 'Такая модель не найдена в '
                                               'базе. Попробуйте '
                                               'ввести другой '
                                               'вариант.')
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

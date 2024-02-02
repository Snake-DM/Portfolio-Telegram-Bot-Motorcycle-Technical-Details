from telebot.types import Message
from database.db_crud import db_customCRUD
from keyboards.inline.pagination import search_result_freeze, message_by_page
from loader import bot
from states.search_states import SearchStates
from custom_requests.api_request import api_request


@bot.message_handler(state=SearchStates.model_year_no)
def model_year_no(message: Message) -> None:
    """
    Function registers a Year parameter (yes/no) and proceeds with option
    "No" in current state.
    Option "Yes" changes state.

    :param message: incoming message from a user
    :return: none
    """
    if message.text.lower().endswith('да'):
        bot.set_state(message.from_user.id,
                      SearchStates.model_year_yes,
                      message.chat.id)
        bot.send_message(message.from_user.id, 'Какой год выпуска?')
    elif message.text.lower().endswith('нет'):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            search_result_iter = api_request("/v1/motorcycles",
                                             {'model': data['model']},
                                             "GET")
        if not search_result_iter:
            bot.send_message(message.from_user.id,
                             'Такая модель не найдена в базе. Попробуйте '
                             'ввести другую модель и/или год выпуска.')
            bot.delete_state(message.from_user.id)
        else:
            # Handle for pagination of a message with results:
            search_result_freeze(search_result_iter)
            message_by_page(message)

            # NOTE: State delete happens in callback function while exit from
            # pagination.

            # TODO
            #  - add this code for large message results
            #  - move this part to function [message_max_length]?

            # for item in answer:
            #     item_for_reply = json.dumps(item, indent=4)

            # Splitting reply to Telegram limit of a single message:
            #     while item_for_reply:
            #         # message for sending (valid length)
            #         bot.send_message(message.from_user.id,
            #                          message_max_length(item_for_reply)[0])
            #         # tail message
            #         item_for_reply = message_max_length(item_for_reply)[1]
            # bot.delete_state(message.from_user.id)
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, 'Неправильный ввод. '
                                               'Введите желаемую команду '
                                               'в формате "/..". '
                                               'Воспользуйтесь командой '
                                               '/help при необходимости.')

    # history log update
    db_customCRUD.log_message(message.from_user.id, message.text)

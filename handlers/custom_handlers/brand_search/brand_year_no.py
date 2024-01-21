from telebot.types import Message, BotCommand

from database.db_crud import db_customCRUD
from keyboards.inline.pagination import message_by_page
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

    if message.text.lower().endswith('да'):
        bot.set_state(message.from_user.id,
                      SearchStates.brand_year_yes,
                      message.chat.id)
        bot.send_message(message.from_user.id, 'Какой год выпуска?')

    elif message.text.lower().endswith('нет'):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            search_result = api_request("/v1/motorcycles",
                                      {'make': data['brand']},
                                      "GET")
        if not search_result:
            bot.send_message(message.from_user.id, 'Такой брэнд не найден в '
                                                   'базе. Попробуйте '
                                                   'ввести другой '
                                                   'вариант.')
            bot.delete_state(message.from_user.id)
        else:
            # TODO Implement pagination
            # Pagination code:

            search_result_total_items = len(list(search_result))
            message_by_page(data=list(search_result),
                            message=message,
                            previous_message=message,
                            page_total=search_result_total_items)


            # page_total = len(list(answer))
            # for item in answer:
            #     item_for_reply = json.dumps(item, indent=4)
            #
            #     page_buttons(message, message, page_total)
            #
            #     bot.send_message(message.from_user.id,
            #                      item_for_reply,
            #                      reply_markup=keyboard_pages)
            #
            #     bot.delete_message(message.from_user.id, previous_message.id)




            # for item in answer:
            #     item_for_reply = json.dumps(item, indent=4)
            #
            #
            # i = 0
            # bot.send_message(
            #         message.from_user.id,
            #         list(answer)[i],
            #         reply_markup=page_buttons(message,
            #                                   previous_message=message,
            #                                   page=i,
            #                                   page_total=len(list(answer))
            #                                   )
            # )
            # bot.delete_message(message.from_user.id,
            #                    previous_message.id)
            #
            #

            # for item in answer:
            #     item_for_reply = json.dumps(item, indent=4)
            #
            #     # TODO move this part to function [message_max_length]?
            #     # Splitting reply to Telegram limit of a single message:
            #     while item_for_reply:
            #         # message for sending (valid length)
            #         bot.send_message(message.from_user.id,
            #                          message_max_length(item_for_reply)[0])
            #         # tail message
            #         item_for_reply = message_max_length(item_for_reply)[1]
            bot.delete_state(message.from_user.id)
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, 'Неправильный ввод. '
                                               'Введите желаемую команду '
                                               'в формате "/..". '
                                               'Воспользуйтесь командой '
                                               '/help при необходимости.')

    # history log update
    db_customCRUD.log_message(message.from_user.id, message.text)

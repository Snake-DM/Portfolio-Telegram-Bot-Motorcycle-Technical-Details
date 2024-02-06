from telebot.types import Message, ReplyKeyboardRemove

from database.db_crud import db_customCRUD
from keyboards.inline.pagination import message_by_page
from loader import bot
from custom_requests.api_request import api_request
from states.search_states import SearchStates


@bot.message_handler(state=SearchStates.brand_year_yes)
def brand_year_yes(message: Message) -> None:
    """
    Function registers a year and provides requested data from the server
    with year parameter "Yes".

    :param message: incoming message from a user
    :return: none
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['year'] = message.text
        search_result_byy = api_request("/v1/motorcycles",
                                    {'make': data['brand'],
                                     'year': data['year']},
                                    "GET")
    if not search_result_byy:
        bot.send_message(message.from_user.id,
                         'Такой брэнд не найден в '
                         'базе этого года. Попробуйте '
                         'ввести другой брэнд и/или '
                         'год выпуска.',
                         reply_markup=ReplyKeyboardRemove())
        bot.delete_state(message.from_user.id)
    else:
        # Handle for pagination of a message with results:
        message_by_page(message=message,
                        result_list=search_result_byy)

        # bot.delete_state(message.from_user.id, message.chat.id)

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

    # history log update
    db_customCRUD.log_message(message.from_user.id, message.text)

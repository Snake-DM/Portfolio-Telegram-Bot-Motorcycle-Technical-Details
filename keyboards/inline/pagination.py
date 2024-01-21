import json
from collections.abc import Iterable

from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           Message)

from loader import bot


def message_by_page(data: list = None,
                    message: Message = None,
                    previous_message: Message = None,
                    page: int = 1,
                    page_total: int = None) -> None:

    if data:
        data_list = data[:]
    if page < 0:
        bot.send_message(message.from_user.id,
                         'Выход из режима просмотра завершён.\n'
                         'Введите команду.')
        bot.delete_state(message.from_user.id, message.chat.id)
    else:

        left = page - 1 if page != 1 else page_total
        right = page + 1 if page != page_total else 1

        keyboard_pages = InlineKeyboardMarkup()

        left_button = InlineKeyboardButton("←",
                                           callback_data=f'to {left}')
        page_button = InlineKeyboardButton(f"{str(page)}/{str(page_total)}",
                                           callback_data='_')
        right_button = InlineKeyboardButton("→",
                                            callback_data=f'to {right}')
        exit_button = InlineKeyboardButton("Exit", callback_data='exit')
        keyboard_pages.add(left_button, page_button, right_button)
        keyboard_pages.add(exit_button)

        result_per_page = json.dumps(data[page - 1], indent=4)
        # result_per_page = data_list[page - 1]
        bot.send_message(message.from_user.id,
                         result_per_page,
                         reply_markup=keyboard_pages)
        bot.delete_message(message.from_user.id, previous_message.id)

# def page_buttons(message,
#                  previous_message=None,
#                  page=1,
#                  page_total=None) -> (
#         InlineKeyboardMarkup):
#
#     left = page - 1 if page != 1 else page_total
#     right = page + 1 if page != page_total else 1
#
#     keyboard_pages = InlineKeyboardMarkup()
#
#     left_button = InlineKeyboardButton("←",
#                                        callback_data=f'to {left}')
#     page_button = InlineKeyboardButton(f"{str(page)}/{str(page_total)}",
#                                        callback_data='_')
#     right_button = InlineKeyboardButton("→",
#                                         callback_data=f'to {right}')
#     keyboard_pages.add(left_button, page_button, right_button)
#     return keyboard_pages


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if 'to' in call.data:
        page = int(call.data.split(' ')[1])
        message_by_page(
                        message=call.message,
                        previous_message=call.message,
                        page=page)
    elif 'exit' in call.data:
        data = []
        page = -1
        message_by_page(
                        message=call.message,
                        previous_message=call.message,
                        page=page)

import json
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           Message)
from loader import bot


result_freeze = dict()


def message_by_page(message: Message,
                    result_list: list = None,
                    page: int = 1) -> None:
    """
    Function uses pagination for long messages. It keeps search result
    as incoming data and passes it to internal function for further pagination
    It sends only 1 (first page)
    :param message: Message
    :param result_list: list
    :param page: int
    :return: None
    """

    global result_freeze

    if result_list:
        result_freeze[message.chat.id] = result_list[:]

    page_data = result_freeze[message.chat.id][page - 1]
    page_total = len(result_freeze[message.chat.id])

    page_text = json.dumps(page_data, indent=2)

    left = page - 1 if page != 1 else page_total
    right = page + 1 if page != page_total else 1

    keyboard_pages = InlineKeyboardMarkup()
    left_button = InlineKeyboardButton('←',
                                       callback_data=f'to {left}')
    page_button = InlineKeyboardButton(f'{str(page)}/{str(page_total)}',
                                       callback_data='_')
    right_button = InlineKeyboardButton('→',
                                        callback_data=f'to {right}')
    exit_button = InlineKeyboardButton('Exit', callback_data='exit')
    keyboard_pages.add(left_button, page_button, right_button)
    keyboard_pages.add(exit_button)

    if message.reply_markup:
        bot.edit_message_text(page_text,
                              message.chat.id,
                              message.message_id,
                              reply_markup=keyboard_pages)
    else:
        bot.send_message(message.chat.id,
                         page_text,
                         reply_markup=keyboard_pages)


@bot.callback_query_handler(func=lambda call: True)
def callback(call) -> None:
    """
    Function handles button pressing in messages with pages.
    :param call: str
    :return: none
    """
    global result_freeze

    if 'to' in call.data:
        new_page = int(call.data.split(' ')[1])
        message_by_page(message=call.message,
                        page=new_page)
    elif 'exit' in call.data:
        del result_freeze[call.message.chat.id]
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)

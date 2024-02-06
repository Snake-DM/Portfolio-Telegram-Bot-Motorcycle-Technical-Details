import json
from typing import Any

from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           Message)
from loader import bot


def message_by_page(message: Message,
                    result_list: Any) -> None:
    """
    Function uses pagination for long messages. It keeps search result
    as incoming data and passes it to internal function for further pagination
    :param message: Message
    :param result_list: list
    :return: None
    """

    result_list_length = len(result_list)

    def send_pages(page: int = 1) -> None:
        """
        Function-paginator extracts page text, creates buttons and sends it.
        :param page: int, page indicator
        :return: none
        """

        print('Текущая страница: ', page - 1, end=';  ')
        print('Длина списка: ', len(result_list))

        page_data = result_list[page - 1]
        page_total = result_list_length

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
        if 'to' in call.data:
            new_page = int(call.data.split(' ')[1])
            send_pages(page=new_page)
        elif 'exit' in call.data:
            result_list.clear()
            bot.delete_message(call.message.chat.id,
                               call.message.message_id)

    return send_pages()

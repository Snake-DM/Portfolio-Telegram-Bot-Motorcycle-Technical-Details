from telebot.types import Message

from database import database
from loader import bot
from states.search_states import SearchStates


@bot.message_handler(commands=["brand"])
def brand_query(message: Message) -> None:
    """
    This handler starts a search by Brand.

    :param message: incoming message from a user
    :return: none
    """
    bot.set_state(message.from_user.id, SearchStates.brand, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название брэнда, '
                                           f'который Вы ищете.')

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )


@bot.message_handler(state=SearchStates.brand)
def get_brand_name(message: Message) -> None:
    """
    Function registers a Brand name and requests a Year parameter (yes/no).

    :param message: incoming message from a user
    :return: none
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['brand'] = message.text
    bot.set_state(message.from_user.id,
                  SearchStates.brand_year_no,
                  message.chat.id)
    bot.send_message(message.from_user.id, 'Желаете указать год выпуска? '
                                           '(да/нет)')

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

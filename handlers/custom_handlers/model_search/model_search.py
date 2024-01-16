from telebot.types import Message

from database import database
from loader import bot
from states.search_states import SearchStates


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
def get_model_name(message: Message) -> None:
    """
    Function registers a Model name and requests a Year parameter (yes/no).

    :param message: incoming message from a user
    :return: none
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['model'] = message.text

        bot.set_state(message.from_user.id,
                      SearchStates.model_year_no,
                      message.chat.id)

    bot.send_message(message.from_user.id, 'Желаете указать год выпуска? '
                                           '(да/нет)')

    # history log update
    database.UserMessageLog.create(
            from_user_id=message.from_user.id,
            user_message=message.text,
    )

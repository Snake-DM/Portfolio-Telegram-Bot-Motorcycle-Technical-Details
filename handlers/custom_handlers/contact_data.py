from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=['start'])
def contact_data(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Здравствуйте, '
                                           f'{message.from_user.username}, '
                                           f'введите свое имя')

@bot.message_handler(state=UserInfoState.name, is_alpha=True)
def get_name(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Благодарю')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text

    bot.send_message(message.from_user.id, 'Введите свой возраст')
    bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)


@bot.message_handler(state=UserInfoState.name, is_alpha=False)
def get_name_wrong(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Имя может содержать только буквы. Попробуйте ещё раз.')


@bot.message_handler(state=UserInfoState.age, is_digit=True)
def get_age(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Благодарю.')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.from_user.id, 'Введите свой опыт вождения '
                                           'мотоцикла.')
    bot.set_state(message.from_user.id,
                  UserInfoState.moto_driving_experience, message.chat.id)


@bot.message_handler(state=UserInfoState.age, is_digit=False)
def get_age_wrong(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Возраст может содержать только цифры. Попробуйте ещё '
                     'раз.')


@bot.message_handler(state=UserInfoState.moto_driving_experience,
                     is_digit=True)
def get_moto_experience(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Благодарю.')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['moto_experience'] = message.text

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ваши данные:\n<b>"
               f"Имя: {data['name']}\n"
               f"Возраст: {data['age']}\n"
               f"Опыт вождения мотоцикла: {data['moto_experience']}\n")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)

    msg = (f"{message.from_user.full_name}!\n"
            f"Выбери параметры поиска мотоциклов через команды.\n"
            f"Для начала используй команду /help.")
    bot.reply_to(message, msg)


@bot.message_handler(state=UserInfoState.moto_driving_experience,
                     is_digit=False)
def get_moto_experience_wrong(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Опыт вождения может содержать '
                                           'только цифры. Попробуйте ещё раз.')


#
# @bot.message_handler(content_types=['contact'],
#                      state=UserInfoState.number)
# def get_number(message: Message) -> None:
#     if message.content_type == 'contact':
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['number'] = message.contact.phone_number
#         text = (f'Спасибо за предоставленную информацию:\n'
#                 f'Имя: {data["name"]}\n '
#                 f'Возраст: {data["age"]}\n '
#                 f'Страна: {data["country"]}\n '
#                 f'Город: {data["city"]}\n '
#                 f'Номер телефона: {data["number"]}\n')
#         bot.send_message(message.from_user.id, text)
#         bot.delete_state(message.from_user.id, message.chat.id)

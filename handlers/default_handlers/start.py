from telebot.types import Message
from loader import bot
from states.contact_info import UserInfoState


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.send_message(message.from_user.id,
                     f'Здравствуйте, {message.from_user.username}!\n'
                     f'Данный бот позволит Вам найти детальную справочную '
                     f'информацию по различным моделям мотоциклов.')
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'\nВведите своё имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Благодарю')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
        bot.send_message(message.from_user.id, 'Введите свой возраст, лет')
    else:
        bot.send_message(message.from_user.id,
                         'Имя может содержать только буквы. Попробуйте ещё раз')


@bot.message_handler(state=UserInfoState.age, is_digit=True)
def get_age(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Благодарю')
    bot.set_state(message.from_user.id,
                  UserInfoState.moto_driving_experience, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.from_user.id, 'Введите свой опыт вождения '
                                           'мотоцикла, лет')


@bot.message_handler(state=UserInfoState.age, is_digit=False)
def get_age_wrong(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     'Возраст может содержать только цифры. Попробуйте '
                     'ещё раз')


@bot.message_handler(state=UserInfoState.moto_driving_experience,
                     is_digit=True)
def get_moto_experience(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Благодарю')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['moto_experience'] = message.text

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ваши данные:\n"
               f"Имя: {data['name']}\n"
               f"Возраст, лет: {data['age']}\n"
               f"Опыт вождения мотоцикла, лет:"
               f" {data['moto_experience']}\n")
        bot.send_message(message.chat.id, msg)

        msg = (f"{data['name']}!\n"
               f"Выберите параметры поиска мотоциклов через команды.\n"
               f"Для начала используйте команду /help.")
        bot.send_message(message.chat.id, msg)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=UserInfoState.moto_driving_experience,
                     is_digit=False)
def get_moto_experience(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Опыт вождения может '
                                           'содержать только цифры. '
                                           'Попробуйте ещё раз.')

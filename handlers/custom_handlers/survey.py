from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Здравствуйте, '
                                           f'{message.from_user.username}, '
                                           f'введите свое имя ')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Благодарю. Введите свой '
                                               'возраст.')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Имя может содержать только '
                                               'буквы')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Благодарю. Введите страну '
                                               'проживания.')
        bot.set_state(message.from_user.id, UserInfoState.country,
                      message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
             data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Возраст может содержать '
                                               'только цифры')


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Благодарю. Введите свой '
                                               'город.')
        bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Страна может содержать только '
                                               'буквы')


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id,
                         'Благодарю. Отправьте свой номер телефона, нажав на кнопку.',
                         reply_markup=request_contact())
        bot.set_state(message.from_user.id, UserInfoState.number,
                      message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Город может содержать только '
                                               'буквы')


@bot.message_handler(content_types=['text', 'contact'],
                      state=UserInfoState.number)
def get_number(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number'] = message.contact.phone_number
        text = (f'Спасибо за предоставленную информацию:\n'
                f'Имя: {data["name"]}\n '
                f'Возраст: {data["age"]}\n '
                f'Страна: {data["country"]}\n '
                f'Город: {data["city"]}\n '
                f'Номер телефона: {data["number"]}\n')
        bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Нажмите на кнопку, '
                                               'чтобы отправить контактную '
                                               'информацию')

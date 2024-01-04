from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    brand = State()
    model = State()

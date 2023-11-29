from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    brand = State()
    brand_year = State()
    model = State()

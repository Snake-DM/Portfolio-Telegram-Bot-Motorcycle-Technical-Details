from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    brand = State()
    brand_year_yes = State()
    brand_year_no = State()
    model = State()
    model_year_yes = State()
    model_year_no = State()

from telebot.handler_backends import State, StatesGroup


class LangCurrencyStates(StatesGroup):
    language = State()
    currency = State()

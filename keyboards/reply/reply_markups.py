from telebot import types

from utils.multilingual import multilingual

def base_reply_markup(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_button_lowprice_hotels = multilingual(locale, 'text_button_lowprice_hotels')
    text_button_hightprice_hotels = multilingual(locale, 'text_button_hightprice_hotels')
    text_button_bestdeal_hotels = multilingual(locale, 'text_button_bestdeal_hotels')
    text_button_history = multilingual(locale, 'text_button_history')

    lowprice_hotels = types.KeyboardButton(text_button_lowprice_hotels)
    hightprice_hotels = types.KeyboardButton(text_button_hightprice_hotels)
    bestdeal_hotels = types.KeyboardButton(text_button_bestdeal_hotels)
    history = types.KeyboardButton(text_button_history)
    keyboard.add(lowprice_hotels, hightprice_hotels)
    keyboard.add(bestdeal_hotels)
    keyboard.add(history)
    return keyboard


def cancel_markup(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_button_cancel_state = multilingual(locale, 'text_button_cancel_state')
    cancel_state = types.KeyboardButton(text_button_cancel_state)
    keyboard.add(cancel_state)
    return keyboard


def choose_language_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton("RU"),
        types.KeyboardButton("EN"),
        types.KeyboardButton("DE"),
        types.KeyboardButton("FR"),
        types.KeyboardButton("IT"),
        types.KeyboardButton("ES")
    ]
    keyboard.add(*buttons)
    return keyboard


def choose_currency_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton("RUB"),
        types.KeyboardButton("EUR"),
        types.KeyboardButton("USD"),
        types.KeyboardButton("GBP"),
        types.KeyboardButton("KZT"),
        types.KeyboardButton("UAH"),
        types.KeyboardButton("CNY"),
        types.KeyboardButton("JPY")
    ]
    keyboard.add(*buttons)
    return keyboard
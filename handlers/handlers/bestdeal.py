from datetime import datetime

from telebot.types import Message
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar

from database.db import Database
from keyboards.reply import reply_markups
from loader import bot
from states.lowprice_states import LowPriceStates
from utils.multilingual import multilingual
from .base import any_state
from .user_data import users_dict

db = Database('database/database.db')


@bot.message_handler(func=lambda message: message.text in ["🧐 Поиск отелей по цене/расположению от центра",
                                                           "🧐 Search for hotels by price/location from the center",
                                                           "🧐 Suche nach Hotels nach Preis/Lage vom Zentrum",
                                                           "🧐 Trouver des Hôtels par prix/emplacement du centre",
                                                           "🧐 Cerca Hotel per Prezzo/posizione dal centro",
                                                           "🧐 Buscar hoteles por precio/ubicación desde el centro"])
@bot.message_handler(commands=['bestdeal'])
def bestdeal_start(message: Message) -> None:
    """
        Функция для запуска сценария поиска отелей, наиболее подходящих по цене и расположению от центра.
    Args:
        :return: None
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    if message.from_user.id in users_dict:
        if users_dict[message.from_user.id].hotel_message is not None:
            bot.delete_message(message.from_user.id, users_dict[message.from_user.id].hotel_message)
            users_dict[message.from_user.id].hotel_message = None
    bot.delete_state(message.from_user.id, message.chat.id)
    text = multilingual(locale, 'base_start')
    bot.send_message(message.from_user.id, text, reply_markup=reply_markups.cancel_markup(locale))
    bot.set_state(message.from_user.id, LowPriceStates.city_data, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sort_order'] = 'DISTANCE_FROM_LANDMARK'
        data['command'] = '/bestdeal'


@bot.message_handler(state=LowPriceStates.price_range)
def get_price_range(message: Message) -> None:
    """
        Функция для получения от пользователя максимальной и минимальной цены, и записи в память.
    Args:
        :return: None
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if 'priceMin' not in data.keys():
                data['priceMin'] = message.text
                max_price_in_data = False
            else:
                data['priceMax'] = message.text
                max_price_in_data = True
        print(message.from_user.id)

        if not max_price_in_data:
            locale_currency_tuple = db.select_lang_currency_user(message.from_user.id)
            currency = locale_currency_tuple[1]
            text = multilingual(locale, 'get_price_range_price_min', currency)
            bot.send_message(message.from_user.id, text)
            bot.set_state(message.from_user.id, LowPriceStates.price_range, message.chat.id)
        else:
            if locale == 'en_US':
                distance_unit_of_measurement = 'ml'
            else:
                distance_unit_of_measurement = 'km'
            text = multilingual(locale, 'get_price_range_max_distance', distance_unit_of_measurement)
            bot.send_message(message.from_user.id, text)
            bot.set_state(message.from_user.id, LowPriceStates.distance_range, message.chat.id)
    else:
        if message.text != 'Отмена':
            bot.set_state(message.from_user.id, LowPriceStates.price_range, message.chat.id)
            text = multilingual(locale, 'get_price_range_valid_error')
            bot.send_message(message.from_user.id, text)
        else:
            any_state(message)


@bot.message_handler(state=LowPriceStates.distance_range)
def get_distance_range(message: Message) -> None:
    """
        Функция для получения от пользователя максимального расстояния до центра, и записи в память.
    Args:
        :return: None
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    if message.text.replace(".", "", 1).isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['max_distance'] = message.text

        bot.set_state(message.from_user.id, LowPriceStates.distance_range, message.chat.id)
        calendar, step = DetailedTelegramCalendar(min_date=datetime.now().date(), locale='ru').build()
        text = multilingual(locale, 'calendar_check_in', LSTEP[step])
        bot.send_message(message.from_user.id, text, reply_markup=calendar)
    else:
        text = multilingual(locale, 'get_distance_range_value_error')
        bot.send_message(message.from_user.id, text)

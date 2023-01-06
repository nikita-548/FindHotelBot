from telebot.types import Message

from database.db import Database
from keyboards.reply import reply_markups
from loader import bot
from states.lowprice_states import LowPriceStates
from utils.multilingual import multilingual
from .user_data import users_dict

db = Database('database/database.db')


@bot.message_handler(func=lambda message: message.text in ["💲💲 Дорогие отели", "💲💲 Expensive hotels",
                                                           "💲💲 Teure Hotels", "💲💲 Hôtels de luxe",
                                                           "💲💲 Hotel costos", "💲💲 Hoteles caros"])
@bot.message_handler(commands=['hightprice'])
def hightprice_start(message: Message) -> None:
    """
        Функция для запуска сценария поиска дорогих отелей.
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
        data['sort_order'] = 'PRICE_HIGHEST_FIRST'
        data['command'] = '/hightprice'
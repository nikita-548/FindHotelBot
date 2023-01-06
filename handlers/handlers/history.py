import re

from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.db import Database
from loader import bot
from utils.multilingual import multilingual
from .user_data import User, users_dict

db = Database('database/database.db')

callback_data_history = CallbackData('action', 'command_date_time_tuple', prefix='history')


@bot.message_handler(func=lambda message: message.text in ['💾 История поиска', '💾 Search history',
                                                           '💾 Suchverlauf', '💾 Historique de la recherche',
                                                           '💾 Cronologia delle ricerche`', '💾 Historial de búsqueda'])
@bot.message_handler(commands=['hystory'])
def hystory_start(message: Message) -> None:
    locale = db.select_locale_user(message.from_user.id)[0]
    command_date_time = db.select_command_date_time_by_user_id(message.from_user.id)
    if message.from_user.id not in users_dict.keys():
        users_dict[message.from_user.id] = User()
    users_dict[message.from_user.id].hotels_ids_dict = {}

    for line in command_date_time:
        new_date_time = re.sub(r':', '.', line['date_time'])
        if (line['command'], new_date_time) not in users_dict[message.from_user.id].hotels_ids_dict.keys():
            users_dict[message.from_user.id].hotels_ids_dict[(line['command'], new_date_time)] = []
        users_dict[message.from_user.id].hotels_ids_dict[(line['command'], new_date_time)].append(line['hotel_id'])

    keyboard = InlineKeyboardMarkup()

    for command_date_time_tuple, hotel_ids in users_dict[message.from_user.id].hotels_ids_dict.items():
        btn = InlineKeyboardButton(text=f'Дата и время: {re.sub(r"[.]", ":", command_date_time_tuple[1])}\n'
                                        f'Команда: {command_date_time_tuple[0]}',
                                   callback_data=callback_data_history.new(
                                       action="show_history",
                                       command_date_time_tuple=command_date_time_tuple))
        keyboard.add(btn)
    if len(users_dict[message.from_user.id].hotels_ids_dict) != 0:
        text = multilingual(locale, 'history_start')
    else:
        text = multilingual(locale, 'history_clean')

    bot.send_message(message.from_user.id, text,
                     reply_markup=keyboard)


move_back_history = CallbackData('action', prefix='move_back')


@bot.callback_query_handler(func=None, config=callback_data_history.filter())
def show_history(call: CallbackData) -> None:
    callback_data = callback_data_history.parse(callback_data=call.data)
    key = eval(callback_data['command_date_time_tuple'])
    hotels_ids = users_dict[call.from_user.id].hotels_ids_dict[key]
    locale = db.select_locale_user(call.from_user.id)[0]
    text = multilingual(locale, 'show_history_base_text', key[0], key[1])

    for hotels_information in db.select_hotel_information_by_hotel_id(hotels_ids):
        for hotel in hotels_information:
            hotel_name = hotel['hotel_name']
            address = hotel['address']
            distance_from_landmark = hotel['distance_from_landmark']
            price = hotel['current_price']
            hotels_information_text = multilingual(locale, 'show_history_information_text',
                                                   hotel_name,
                                                   address,
                                                   distance_from_landmark,
                                                   price
                                                   )
            text += hotels_information_text

    keyboard = InlineKeyboardMarkup()

    move_back_btn = InlineKeyboardButton('<< Вернуться', callback_data=move_back_history.new(action='back'))
    keyboard.add(move_back_btn)
    bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                          text=text, reply_markup=keyboard)

    users_dict[call.from_user.id].message_id_history = call.message.message_id


@bot.callback_query_handler(func=None, config=move_back_history.filter())
def go_back_history(call) -> None:
    command_date_time = db.select_command_date_time_by_user_id(call.from_user.id)
    if call.from_user.id not in users_dict.keys():
        users_dict[call.from_user.id] = User()
    users_dict[call.from_user.id].hotels_ids_dict = {}

    for line in command_date_time:
        new_date_time = re.sub(r':', '.', line['date_time'])
        if (line['command'], new_date_time) not in users_dict[call.from_user.id].hotels_ids_dict.keys():
            users_dict[call.from_user.id].hotels_ids_dict[(line['command'], new_date_time)] = []
        users_dict[call.from_user.id].hotels_ids_dict[(line['command'], new_date_time)].append(line['hotel_id'])

    keyboard = InlineKeyboardMarkup()

    for command_date_time_tuple, hotel_ids in users_dict[call.from_user.id].hotels_ids_dict.items():
        btn = InlineKeyboardButton(text=f'Дата и время: {re.sub(r"[.]", ":", command_date_time_tuple[1])}\n'
                                        f'Команда: {command_date_time_tuple[0]}',
                                   callback_data=callback_data_history.new(
                                       action="show_history",
                                       command_date_time_tuple=command_date_time_tuple))
        keyboard.add(btn)
    bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Выберите дату и команду, чтобы посмотреть найденные отели:',
                          reply_markup=keyboard)

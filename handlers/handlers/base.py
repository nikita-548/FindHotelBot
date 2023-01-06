import re
from datetime import datetime

from telebot import AdvancedCustomFilter, custom_filters
from telebot.callback_data import CallbackDataFilter
from telebot.types import CallbackQuery, InputMediaPhoto, Message
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar

from database.db import Database
from keyboards.inline import inline_markups
from keyboards.reply import reply_markups
from loader import bot
from states.lowprice_states import LowPriceStates
from utils.multilingual import multilingual
from .load_data_api import load_data_cities, load_data_hotels, load_data_photo
from .user_data import User, users_dict

db = Database('database/database.db')


@bot.message_handler(func=lambda message: message.text in ["Отмена ❌", 'Cancel ❌',
                                                           'Annullierung ❌', 'Annulation ❌', 'Cancellazione ❌'
                                                           'Cancelación ❌'])
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message: Message) -> None:
    """
        Функция для закрытия всех состояний.
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    text = multilingual(locale, 'any_state')
    bot.send_message(message.chat.id, text, reply_markup=reply_markups.base_reply_markup(locale))
    bot.delete_state(message.from_user.id, message.chat.id)


class CitiesCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


@bot.message_handler(state=LowPriceStates.city_data)
def city_founding(message: Message) -> None:
    """
        Функция вывода списка городов, полученных по запросу API, на основе полученного от пользователя названия города.
    """
    locale = db.select_locale_user(message.from_user.id)[0]

    sticker = bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIE-mL8jCsZfhmU2HlgnVSb9cYvT327AAJFAANZu_wl-9SkNOET-OspBA')

    city_for_search = message.text

    data = load_data_cities(city_for_search=city_for_search, user_id=message.from_user.id)

    if (data is None) or not ('suggestions' in data):
        text = multilingual(locale, 'city_founding_api_error')
        bot.send_message(message.from_user.id, text)
        any_state(message)
    else:
        cities = data['suggestions'][0]['entities']
        if len(cities) != 0:
            bot.delete_message(chat_id=sticker.chat.id, message_id=sticker.id)
            pattern = r"<span{1}.*>(\b.*\b)</span{1}>(.*)"

            cities_destination_id = {}

            for city in cities:
                if 'span' in city['caption']:
                    city_caption = ''.join(re.findall(pattern, city['caption'])[0])
                else:
                    city_caption = city['caption']
                cities_destination_id[city['destinationId']] = city_caption
            text = multilingual(locale, 'city_founding')
            bot.send_message(message.chat.id, text=text,
                             reply_markup=inline_markups.cities_markups(cities_destination_id))

        else:
            bot.delete_message(chat_id=sticker.chat.id, message_id=sticker.id)
            text = multilingual(locale, 'city_founding_zero')
            bot.send_message(message.chat.id, text=text)


def locale_ru_calendar(word) -> str:
    LSTEP_ru = {
        'year': 'год',
        'month': 'месяц',
        'day': 'день'
    }
    return LSTEP_ru[word]


@bot.callback_query_handler(func=None, config=inline_markups.callback_data_city_id.filter())
def get_city_id(call: CallbackQuery) -> None:
    """
        Функция для обработки выбранного города и формирования календаря.
    """
    locale = db.select_locale_user(call.from_user.id)[0]

    callback_data = inline_markups.callback_data_city_id.parse(callback_data=call.data)
    text = multilingual(locale, 'get_city_id_send_name_city', callback_data['city_name'])
    bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                          text=text)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        sort_order = data['sort_order']

    if sort_order == 'DISTANCE_FROM_LANDMARK':
        locale_currency_tuple = db.select_lang_currency_user(call.from_user.id)
        currency = locale_currency_tuple[1]
        text = multilingual(locale, 'get_city_id_distance_from_landmark', currency)
        bot.send_message(call.from_user.id, text)
        bot.set_state(call.from_user.id, LowPriceStates.price_range, call.message.chat.id)  # BESTDEAL
    else:
        calendar, step = DetailedTelegramCalendar(min_date=datetime.now().date(), locale='ru').build()
        step = multilingual(locale, LSTEP[step])
        text = multilingual(locale, 'calendar_check_in', step)
        bot.send_message(call.from_user.id, text, reply_markup=calendar)

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['city_id'] = int(callback_data['city_id'])


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def calendar_func(call: CallbackQuery) -> None:
    """
        Функция для получения данных из календаря и записи их в память.
    """
    locale = db.select_locale_user(call.from_user.id)[0]
    result, key, step = DetailedTelegramCalendar(min_date=datetime.now().date(), locale='ru').process(call.data)
    step = multilingual(locale, LSTEP[step])
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        if 'start_date' in data:
            text = multilingual(locale, 'calendar_check_out', step)
        else:
            text = multilingual(locale, 'calendar_check_in', step)

    if not result and key:
        bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            if 'start_date' not in data:
                data['start_date'] = result
                calendar, step = DetailedTelegramCalendar(min_date=data['start_date'], locale='ru').build()
                step = multilingual(locale, LSTEP[step])
                text = multilingual(locale, 'calendar_check_out', step)
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      text=text, reply_markup=calendar)
            else:
                data['end_date'] = result
                text = multilingual(locale, 'calendar_results', data['start_date'], data['end_date'])
                bot.edit_message_text(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      text=text)
                text = multilingual(locale, 'calendar_func_end')
                bot.send_message(call.from_user.id, text)
                bot.set_state(call.from_user.id, LowPriceStates.adults_number, call.message.chat.id)


@bot.message_handler(state=LowPriceStates.adults_number)
def adults_number_func(message: Message) -> None:
    """
        Фкнция для получения введенного пользователем количества взрослых гостей отеля и записи в память.
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    if message.text.isdigit():
        bot.set_state(message.from_user.id, LowPriceStates.check_data, message.chat.id)
        text = multilingual(locale, 'adults_number_func')
        bot.send_message(message.from_user.id, text)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults_number'] = int(message.text)
    else:
        text = multilingual(locale, 'asults_number_valid_error')
        bot.send_message(message.from_user.id, text)


@bot.message_handler(state=LowPriceStates.check_data)
def check_data_func(message: Message) -> None:
    """
        Фкнция для подтверждения введенных данных.
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number_hotels'] = int(message.text)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            start_date = data['start_date']
            end_date = data['end_date']
            adults_number = data['adults_number']
            sort_order = data['sort_order']
        text = multilingual(locale, 'check_data_func_base_info', start_date, end_date, adults_number)

        if sort_order == 'DISTANCE_FROM_LANDMARK':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                priceMin = data['priceMin']
                priceMax = data['priceMax']
                max_distance = data['max_distance']
            distance_from_landmark_text = multilingual(locale, 'check_data_distance_from_landmark_text', priceMin,
                                                       priceMax, max_distance)
            text += distance_from_landmark_text
        text = multilingual(locale, 'check_data_func', text)
        bot.send_message(message.from_user.id, text, reply_markup=inline_markups.check_data_markups())
    else:
        text = multilingual(locale, 'check_data_func_valid_error')
        bot.send_message(message.from_user.id, text)


@bot.callback_query_handler(func=None, config=inline_markups.callback_data_check_data.filter())
def get_answer_check_data(call: CallbackQuery) -> None:
    """
        Функция для обработки результата ответа подтверждения введенных данных.
    """
    locale = db.select_locale_user(call.from_user.id)[0]
    callback_data = inline_markups.callback_data_check_data.parse(callback_data=call.data)
    answer = callback_data['answer']
    bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
    if answer == 'yes':
        show_hotels_func(call)
    elif answer == 'no':
        text = multilingual(locale, 'get_answer_check_data_repeat')
        bot.send_message(call.from_user.id, text)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            del data['start_date']
            del data['end_date']
            del data['adults_number']
            sort_order = data['sort_order']
            if sort_order == 'DISTANCE_FROM_LANDMARK':
                del data['priceMin']
                del data['priceMax']
                del data['max_distance']

        if sort_order == 'DISTANCE_FROM_LANDMARK':
            text = multilingual(locale, 'get_answer_check_data_answer_no_distance')
            bot.send_message(call.from_user.id, text)
            bot.set_state(call.from_user.id, LowPriceStates.price_range, call.message.chat.id)
        else:
            calendar, step = DetailedTelegramCalendar(min_date=datetime.now().date(), locale='ru').build()
            step = multilingual(locale, LSTEP[step])
            text = multilingual(locale, 'calendar_check_in', step)

            bot.send_message(call.from_user.id, text, reply_markup=calendar)


def show_hotels_func(call: CallbackQuery) -> None:
    """
        Функция для формирования списка найденных отелей по id города.
    """
    locale = db.select_locale_user(call.from_user.id)[0]
    users_dict[call.from_user.id] = User()
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        start_date = data['start_date']
        end_date = data['end_date']
        city_id = data['city_id']
        adults_number = data['adults_number']
        number_hotels = data['number_hotels']
        sort_order = data['sort_order']
        command = data['command']
    sticker = bot.send_sticker(call.from_user.id,
                               'CAACAgIAAxkBAAIE-mL8jCsZfhmU2HlgnVSb9cYvT327AAJFAANZu_wl-9SkNOET-OspBA')
    if sort_order == 'DISTANCE_FROM_LANDMARK':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            priceMin = data['priceMin']
            priceMax = data['priceMax']
            max_distance = data['max_distance']

        hotels = load_data_hotels(sort_order=sort_order, user_id=call.from_user.id, city_id=city_id,
                                  number_hotels=number_hotels, start_date=start_date, end_date=end_date,
                                  adults_number=adults_number, priceMin=priceMin, priceMax=priceMax)

    else:
        hotels = load_data_hotels(sort_order=sort_order, user_id=call.from_user.id, city_id=city_id,
                                  number_hotels=number_hotels, start_date=start_date, end_date=end_date,
                                  adults_number=adults_number)

    bot.delete_message(chat_id=sticker.chat.id, message_id=sticker.id)

    if hotels is None:
        text = multilingual(locale, 'show_hotels_func_api_error')
        bot.send_message(call.from_user.id, text)
    else:
        if sort_order == 'DISTANCE_FROM_LANDMARK':
            hotels = list(filter(lambda hotel_i:
                                 float((hotel_i['landmarks'][0]['distance'].split())[0].replace(",", ".", 1))
                                 <= float(max_distance),
                                 hotels))

        if len(hotels) != 0:
            for hotel in hotels:
                days = (end_date - start_date).days
                total_cost_float = days * float(hotel['ratePlan']['price']['exactCurrent'])
                total_cost_str = str(total_cost_float) + '$'

                if 'optimizedThumbUrls' in hotel:
                    url_photo = hotel['optimizedThumbUrls']['srpDesktop']
                else:
                    url_photo = 'https://i.pinimg.com/originals/57/43/f9/5743f946f92d75eef89496b867d9e6df.png'

                users_dict[call.from_user.id].info_hotels = \
                    {'hotel_id': hotel['id'], 'base_photo_hotel': url_photo,
                     'name': hotel['name'], 'rating': hotel['starRating'],
                     'address': hotel['address'][list(hotel['address'].keys())[0]],
                     'distance_landmark': hotel['landmarks'][0]['distance'],
                     'price': hotel['ratePlan']['price']['current'], 'total_price': total_cost_str}

            hotels_list = users_dict[call.from_user.id].info_hotels
            db.update_information_about_hotel(hotels_list)

            hotel_id_list = [hotel['hotel_id'] for hotel in hotels_list]
            db.update_search_history(call.from_user.id, command, hotel_id_list)

            len_of_hotels_list = len(hotels_list)
            hotel_id_in_list = 0
            start_hotel = hotels_list[hotel_id_in_list]
            caption = multilingual(locale, 'caption_hotel',
                                   start_hotel['name'],
                                   start_hotel['rating'],
                                   start_hotel['address'],
                                   start_hotel['distance_landmark'],
                                   start_hotel['price'],
                                   start_hotel['total_price'],
                                   hotel_id_in_list + 1,
                                   len_of_hotels_list)

            message_hotel = bot.send_photo(chat_id=call.from_user.id, photo=start_hotel['base_photo_hotel'],
                                           caption=caption,
                                           reply_markup=inline_markups.next_back_hotels_markups(
                                               hotel_id_in_list=0, hotel_id=start_hotel['hotel_id']
                                           ))

            users_dict[call.from_user.id].current_hotel_id_in_list = hotel_id_in_list
            users_dict[call.from_user.id].hotel_message = message_hotel.message_id
        else:
            text = multilingual(locale, 'show_hotels_func_zero_func')
            bot.send_message(call.from_user.id, text)
    bot.delete_state(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=None,
                            config=inline_markups.callback_data_get_hotel_photos.filter(action=['<<', '>>', 'close']))
def flipper_hotels(call: CallbackQuery) -> None:
    """
        Функция для перелистывания отелей.
    """
    locale = db.select_locale_user(call.from_user.id)[0]
    callback_data = inline_markups.callback_data_get_hotel_photos.parse(callback_data=call.data)
    current_hotel_id_in_list = callback_data['hotel_id_in_list']
    action = callback_data['action']
    info_hotels = users_dict[call.from_user.id].info_hotels
    len_hotels = len(info_hotels)

    if action in ('>>', '<<'):
        if action == '>>':
            new_hotel_id_in_list = (int(current_hotel_id_in_list) + 1) % int(len_hotels)
        else:
            new_hotel_id_in_list = (int(current_hotel_id_in_list) - 1) % int(len_hotels)

        users_dict[call.from_user.id].current_hotel_id_in_list = new_hotel_id_in_list
        info_hotel = info_hotels[int(new_hotel_id_in_list)]
        photo = info_hotel['base_photo_hotel']
        caption = multilingual(locale, 'caption_hotel',
                               info_hotel['name'],
                               info_hotel['rating'],
                               info_hotel['address'],
                               info_hotel['distance_landmark'],
                               info_hotel['price'],
                               info_hotel['total_price'],
                               new_hotel_id_in_list + 1,
                               len_hotels)

        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=InputMediaPhoto(photo, caption=caption),
                               reply_markup=inline_markups.next_back_hotels_markups(
                                   hotel_id_in_list=new_hotel_id_in_list,
                                   hotel_id=info_hotels[new_hotel_id_in_list]['hotel_id']
                               ))
    elif action == 'close':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        text = multilingual(locale, 'flipper_hotels_close')
        users_dict[call.from_user.id].hotel_message = None
        bot.send_message(call.from_user.id, text, reply_markup=reply_markups.base_reply_markup(locale))


@bot.callback_query_handler(func=None,
                            config=inline_markups.callback_data_get_hotel_photos.filter(action=['show_photos']))
def get_numbers_photo(call: CallbackQuery) -> None:
    """
        Функция для получения числа фотографий, необходимых для вывода пользователю.
    """
    locale = db.select_locale_user(call.from_user.id)[0]
    text = multilingual(locale, 'get_numbers_photo')
    number_photo_message = bot.send_message(call.from_user.id, text)
    bot.set_state(call.from_user.id, LowPriceStates.show_photos, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['number_photo_message_id'] = number_photo_message.message_id


@bot.message_handler(state=LowPriceStates.show_photos)
def show_photos(message: Message) -> None:
    """
        Функция для отображения фотографий.
    """
    locale = db.select_locale_user(message.from_user.id)[0]
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            number_photo_message_id = data['number_photo_message_id']
            del data['number_photo_message_id']

        bot.delete_message(chat_id=message.chat.id, message_id=number_photo_message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        sticker = bot.send_sticker(message.from_user.id,
                                   'CAACAgIAAxkBAAIE-mL8jCsZfhmU2HlgnVSb9cYvT327AAJFAANZu_wl-9SkNOET-OspBA')

        current_hotel_id_in_list = users_dict[message.from_user.id].current_hotel_id_in_list
        info_hotels = users_dict[message.from_user.id].info_hotels
        real_hotel_id = info_hotels[int(current_hotel_id_in_list)]['hotel_id']
        photo_data = load_data_photo(real_hotel_id)

        if photo_data is not None:
            photos_links = tuple(
                map(lambda photo_i: re.sub(r'{size}', photo_i['sizes'][0]['suffix'], photo_i['baseUrl']),
                    photo_data['hotelImages'][:int(message.text)]))
            bot.delete_message(chat_id=sticker.chat.id, message_id=sticker.id)

            id_photo = 0
            photo_url = photos_links[id_photo]

            hotel_message = users_dict[message.from_user.id].hotel_message
            bot.edit_message_media(chat_id=message.chat.id, message_id=hotel_message,
                                   media=InputMediaPhoto(photo_url),
                                   reply_markup=inline_markups.next_back_photos_markups(id_photo))

            users_dict[message.from_user.id].photos = photos_links
            bot.delete_state(message.from_user.id, message.chat.id)

        else:
            bot.delete_message(chat_id=sticker.chat.id, message_id=sticker.id)
            text = multilingual(locale, 'show_photos_zero')
            bot.send_message(message.from_user.id, text=text, timeout=1)
            bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.set_state(message.from_user.id, LowPriceStates.show_photos, message.chat.id)
        text = multilingual(locale, 'show_photos_valid_error')
        bot.send_message(message.from_user.id, text)


@bot.callback_query_handler(func=None, config=inline_markups.callback_data_flipper.filter())
def flipper_photos(call: CallbackQuery) -> None:
    """
        Функция для перелистывания фотографий.
    """
    locale = db.select_locale_user(call.from_user.id)[0]
    callback_data = inline_markups.callback_data_flipper.parse(callback_data=call.data)
    action = callback_data['action']
    current_photo_id = callback_data['number_photo']

    photos_links = users_dict[call.from_user.id].photos

    number_of_photos = len(photos_links)
    close_gallery = False
    if action == '>>':
        new_id_photo = (int(current_photo_id) + 1) % int(number_of_photos)
        photo_link = photos_links[new_id_photo]
    elif action == '<<':
        new_id_photo = (int(current_photo_id) - 1) % int(number_of_photos)
        photo_link = photos_links[new_id_photo]
    elif action == 'close':
        close_gallery = True

    if close_gallery:
        new_hotel_id_in_list = users_dict[call.from_user.id].current_hotel_id_in_list
        info_hotel_s = users_dict[call.from_user.id].info_hotels
        info_hotel = info_hotel_s[int(new_hotel_id_in_list)]
        photo = info_hotel['base_photo_hotel']
        caption = multilingual(locale, 'caption_hotel',
                               info_hotel['name'],
                               info_hotel['rating'],
                               info_hotel['address'],
                               info_hotel['distance_landmark'],
                               info_hotel['price'],
                               info_hotel['total_price'],
                               new_hotel_id_in_list + 1,
                               len(info_hotel_s))

        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=InputMediaPhoto(photo, caption=caption),
                               reply_markup=inline_markups.next_back_hotels_markups(
                                   hotel_id_in_list=new_hotel_id_in_list,
                                   hotel_id=info_hotel['hotel_id']
                               ))
    else:
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=InputMediaPhoto(photo_link),
                               reply_markup=inline_markups.next_back_photos_markups(new_id_photo))


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(CitiesCallbackFilter())

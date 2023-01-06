from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

callback_data_flipper = CallbackData('action', 'number_photo', prefix='photos')


def next_back_photos_markups(number_photo):
    keyboard = InlineKeyboardMarkup()
    next_photo = InlineKeyboardButton(text='>>',
                                      callback_data=callback_data_flipper.new(action='>>',
                                                                              number_photo=number_photo))
    back_photo = InlineKeyboardButton(text='<<',
                                      callback_data=callback_data_flipper.new(action='<<',
                                                                              number_photo=number_photo))
    keyboard.add(back_photo, next_photo)

    close_button = InlineKeyboardButton(text='Закрыть галлерею',
                                        callback_data=callback_data_flipper.new(action='close',
                                                                                number_photo=number_photo))
    keyboard.add(close_button)
    return keyboard


callback_data_city_id = CallbackData('city_id', 'city_name', prefix='cities')


def cities_markups(dict_cities: dict):
    keyboard = InlineKeyboardMarkup()
    for key, value in dict_cities.items():
        city_name = value.split(',')[0]
        key_byte_array = key.encode(encoding="UTF-16")
        value_byte_array = city_name.encode(encoding="UTF-16")
        sum_byte_array = len(key_byte_array) + len(value_byte_array)
        if sum_byte_array > 64:
            byte_slice = 60 - len(key_byte_array)
            new_value_byte_array = value_byte_array[:byte_slice]
            city_name = new_value_byte_array.decode(encoding="UTF-16")
            city_name += '...'
        switch_button = InlineKeyboardButton(text=value,
                                             callback_data=callback_data_city_id.new(city_id=key, city_name=city_name))
        keyboard.add(switch_button)
    return keyboard


callback_data_get_hotel_photos = CallbackData('hotel_id_in_list', 'action', prefix='hotels')


def next_back_hotels_markups(hotel_id_in_list, hotel_id):
    keyboard = InlineKeyboardMarkup()

    next_photo = InlineKeyboardButton(text='>>',
                                      callback_data=callback_data_get_hotel_photos.new(action='>>',
                                                                                       hotel_id_in_list=hotel_id_in_list))
    back_photo = InlineKeyboardButton(text='<<',
                                      callback_data=callback_data_get_hotel_photos.new(action='<<',
                                                                                       hotel_id_in_list=hotel_id_in_list))

    keyboard.add(back_photo, next_photo)

    get_photos_button = InlineKeyboardButton(text='📸 Посмотреть фото',
                                             callback_data=callback_data_get_hotel_photos.new(
                                                 hotel_id_in_list=hotel_id_in_list,
                                                 action='show_photos'))
    keyboard.add(get_photos_button)

    hotel_link = InlineKeyboardButton(text='🌐 Забронировать', url=f'http://hotels.com/ho{hotel_id}')
    keyboard.add(hotel_link)

    close_hotels = InlineKeyboardButton(text='Закрыть', callback_data=callback_data_get_hotel_photos.new(
                                                 hotel_id_in_list=hotel_id_in_list,
                                                 action='close'))
    keyboard.add(close_hotels)

    return keyboard


callback_data_check_data = CallbackData('answer', prefix='check_data')


def check_data_markups():
    keyboard = InlineKeyboardMarkup()
    positive_answer = InlineKeyboardButton(text='Всё верно ✅', callback_data=callback_data_check_data.new(answer='yes'))
    negative_answer = InlineKeyboardButton(text='Заполнить снова ❌',
                                           callback_data=callback_data_check_data.new(answer='no'))
    keyboard.add(positive_answer, negative_answer)
    return keyboard

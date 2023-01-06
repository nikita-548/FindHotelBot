import json
from typing import Iterable, Optional
import requests

from config_data import config
from database.db import Database

db = Database('database/database.db')


def load_data(url: str, querystring: dict) -> Optional[str]:

    headers = {
        'x-rapidapi-key': config.RAPID_API_KEY,
        'x-rapidapi-host': "hotels4.p.rapidapi.com"
    }
    """
    Функция для загрузки данных из API.
    Args:
        :param url: (str) ссылка с конечной точкоц API
        :param querystring: (dict) словарь, который содержит информацию, необходимую для получения данных по API
        :return: python object
    """
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
    except Exception as e:
        print(e)


def load_data_cities(city_for_search, user_id) -> Optional[str]:

    """
    Функция для возврата списка городов.

    Args:
        :param city_for_search: (str) название города
        :param user_id: (int) id пользователя
        :return: load_data(url=url, headers=headers, querystring=querystring)
    """
    url = 'https://hotels4.p.rapidapi.com/locations/v2/search'

    locale_currency_tuple = db.select_lang_currency_user(user_id)
    locale = locale_currency_tuple[0]
    currency = locale_currency_tuple[1]

    querystring = {
        "query": city_for_search, "locale": locale, "currency": currency
    }

    return load_data(url=url, querystring=querystring)


def generator_page_size(number_of_page, number_of_hotels) -> Iterable:
    """
    Генератор размера страниц.

    Args:
        :param number_of_page: (int) количество страиц
        :param number_of_hotels: (int) общее количество отелей
        :return: Iterable
    """
    for page in range(number_of_page):
        page_size = 0
        for hotel in range(number_of_hotels):
            page_size += 1
            if page_size == 25:
                break
        number_of_hotels -= 25
        yield page_size


def load_data_hotels(sort_order, user_id, city_id, number_hotels, start_date, end_date, adults_number, **kwargs) -> Optional[list]:
    """
    Функция для возврата списка отелей.
    Args:
        :param sort_order: тип сортировки данных
        :param user_id: (int) id пользователя
        :param city_id: id города
        :param number_hotels: количество отелей
        :param start_date: дата заселения
        :param end_date: дата выселения
        :param adults_number: количество взрослых людей в номере
        :param kwargs: значения priceMin, priceMax
        :return: hotels_data
        :rtype: list
    """

    url = 'https://hotels4.p.rapidapi.com/properties/list'

    locale_currency_tuple = db.select_lang_currency_user(user_id)
    locale = locale_currency_tuple[0]
    currency = locale_currency_tuple[1]

    querystring = {
        "destinationId": city_id, "pageNumber": "1",
        "checkIn": start_date, "checkOut": end_date, "adults1": adults_number,
        "sortOrder": sort_order, "locale": locale, "currency": currency
    }

    if sort_order == 'DISTANCE_FROM_LANDMARK':
        querystring["priceMin"] = kwargs['priceMin']
        querystring["priceMax"] = kwargs['priceMax']
        querystring["sortOrder"] = 'DISTANCE_FROM_LANDMARK|PRICE'
        querystring["landmarkIds"] = 'City center'

    hotels_data = []

    number_of_page = int(-1 * (int(number_hotels)/25) // 1 * -1)
    page_sizes = [size for size in generator_page_size(number_of_page, int(number_hotels))]

    for page, page_size in zip(range(1, number_of_page+1), page_sizes):
        querystring['pageNumber'] = page
        querystring['pageSize'] = page_size

        result = load_data(url=url, querystring=querystring)
        if result is None:
            return result
        hotels = result['data']['body']['searchResults']['results']
        hotels_data.extend(hotels)
    return hotels_data


def load_data_photo(hotel_id) -> Optional[str]:
    """
    Функция для возврата загруженных данных по API.
    :param hotel_id: id отеля
    :return: load_data(url=url, headers=headers, querystring=querystring)
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}

    return load_data(url=url, querystring=querystring)

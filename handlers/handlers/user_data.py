users_dict = {}


class User:
    """
        Базовый класс для хранения временных данных пользователя.
    """
    def __init__(self):
        self.__hotel_message = None
        self.__info_hotels = None
        self.__current_hotel_id_in_list = None
        self.__photos_links = None
        self.__hotels_ids_dict = None
        self.__message_id_history = None

    @property
    def message_id_history(self) -> int:
        """
        Геттер для получения id сообщения с историей поиска.
        Args:
            :return: self.__message_id_history
            :rtype: int
        """
        return self.__message_id_history

    @message_id_history.setter
    def message_id_history(self, message_id_history: int) -> None:
        """
        Сеттер для записи id сообщения с историей поиска.
        Args:
            :param message_id_history: (int) идентификатор сообщения с историей поиска
        """
        self.__message_id_history = message_id_history

    @property
    def hotels_ids_dict(self) -> list:
        """
        Геттер для получения идентификаторов отелей.
        :return: self.__hotels_ids_dict
        :rtype: list
        """
        return self.__hotels_ids_dict

    @hotels_ids_dict.setter
    def hotels_ids_dict(self, hotels_ids_dict: dict) -> None:
        """
        Сеттер для записи идентификаторов отелей.
        Args:
            :param hotels_ids_dict: (dict) словарь идентификаторов
        """
        self.__hotels_ids_dict = hotels_ids_dict

    @property
    def current_hotel_id_in_list(self) -> int:
        """
            Геттер для получения текущего id отеля в списке отелей.
        Args:
            :return: self.__current_hotel_id_in_list
            :rtype: int
        """

        return self.__current_hotel_id_in_list

    @current_hotel_id_in_list.setter
    def current_hotel_id_in_list(self, hotel_id_in_list: int) -> None:
        """
           Сеттер для записи текущего id отеля в списке отелей.
        Args:
            :param hotel_id_in_list: (int) id отеля в списке
            :return: None
        """

        self.__current_hotel_id_in_list = hotel_id_in_list

    @property
    def info_hotels(self) -> list:
        """
            Геттер для получения списка отелей. Список состоит из словарей с информацией о каждом отеле.
        Args:
            :return: self.__info_hotels
            :rtype: list
        """

        return self.__info_hotels

    @info_hotels.setter
    def info_hotels(self, hotels_info: list) -> None:
        """
            Сеттер для записи списка отелей. Список состоит из словарей с информацией о каждом отеле.
        Args:
            :param hotels_info: (list) список из словарей с информацией о каждом отеле
            :return: None
        """

        if self.__info_hotels is None:
            self.__info_hotels = []
        self.__info_hotels.append(hotels_info)

    @property
    def photos(self) -> list:
        """
            Геттер для получения списка ссылок фотографий отеля.
        Args:
            :return:  self.__photos_links
        """
        return self.__photos_links

    @photos.setter
    def photos(self, photos_links: list) -> None:
        """
            Сеттер для записи списка ссылок фотографий отеля.
        Args:
            :param photos_links: (list) список ссылок фотографий отеля
            :return: None
        """
        self.__photos_links = photos_links

    @property
    def hotel_message(self) -> int:
        """
            Геттер для получения id сообщения с отелями.
        Args:
            :return: self.__hotel_message
            :rtype: int
        """
        return self.__hotel_message

    @hotel_message.setter
    def hotel_message(self, hotel_message_id: int) -> None:
        """
            Сеттер для записи id сообщения с отелями.
            Нужен для того, чтобы изменить данное сообщение, после выхода из галлереи фотографий отеля.
        Args:
            :param hotel_message_id: (int) id сообщения с отелями
            :return: None
        """
        self.__hotel_message = hotel_message_id


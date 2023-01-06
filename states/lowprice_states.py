from telebot.handler_backends import State, StatesGroup


class LowPriceStates(StatesGroup):
    """
        Машина состояний LowPriceStates. Родитель StatesGroup.
        Используется для сбора параметров необходимого отеля. (Город/Дата, Количетсво взрослых, Количество отелей).
    """
    # Just name variables differently
    city_data = State()  # creating instances of State class is enough from now
    price_range = State()
    distance_range = State()
    adults_number = State()
    check_data = State()
    show_hotels = State()
    show_photos = State()


class ShowPhotosStates(StatesGroup):
    show_photos = State()

def multilingual(locale, key, *args):
    multilingual_messages = {
        'ru_RU': {
            'any_state': 'Вы вышли из сценария',
            'city_founding': '🌆 Выберите город из списка:',
            'city_founding_zero': 'В базе данных Hotels.com нет городов с таким названием',
            'city_founding_api_error': 'Ошибка API. Повторите попытку позже',
            'get_city_id_send_name_city': '🌆 Город: {}',
            'get_city_id_distance_from_landmark': '💵 Отправьте минимальную цену за ночь ({}):',
            'calendar_lang': 'ru',
            'calendar_check_in': '📆 Выберите {} заезда',
            'calendar_check_out': '📆 Выберите {} отъезда',
            'calendar_results': '🛬 Дата заезда: {}\n'
                                '🛫 Дата отъезда: {}\n',
            'month': 'месяц',
            'day': 'день',
            'year': 'год',
            'calendar_func_end': '💃🕺 Введите количество взрослых в номере:',
            'adults_number_func': '🏨🏨🏨 Максимальное количество отелей:',
            'asults_number_valid_error': 'Пожалуйста, введите число',
            'check_data_func_base_info': '\n🛬 Дата заезда: {}\n🛫 Дата отъезда: {}'
                                         '\n💃🕺 Количество взврослых: {}',
            'check_data_distance_from_landmark_text': '\n💵Минимальная стоимость проживания за ночь: {}'
                                                      '\n💵Максимальная стоимость проживания за ночь: {}'
                                                      '\n📍Максимальное расстояние до центра: {}',
            'check_data_func': 'Проверьте введенные данные: {}',
            'check_data_func_valid_error': 'Пожалуйста, введите число',
            'get_answer_check_data_repeat': 'Заполните анкету снова',
            'get_answer_check_data_answer_no_distance': '💵 Отправьте минимальную цену за ночь.',
            'show_hotels_func_api_error': 'Ошибка API. Повторите попытку позже',
            'caption_hotel': '🏨 {}\n⭐️Рейтинг: {}\n📫 Адрес: {}\n'
                             '📍 Расстояние до центра: {}\n'
                             '💲 Стоимость за ночь: {}\n💲💲Стоимость за весь период: '
                             '{}\nОтель {} из {}',
            'show_hotels_func_zero_func': 'Отелей с такими параметрами не нашлось.',
            'flipper_hotels_close': 'Просмотр отелей закрыт',
            'get_numbers_photo': 'Необходимое количество фотографий:',
            'show_photos_zero': 'Фотографий этого отеля нет.',
            'show_photos_valid_error': 'Необходимо ввести число',
            'base_start': '🌆 Отправьте боту город для поиска:',
            'get_price_range_price_min': '💵 Отправьте максимальную цену за ночь ({}):',
            'get_price_range_max_distance': '📍 Отправьте максимальное расстояние до центра ({}):',
            'get_price_range_valid_error': 'Пожалуйста, введите число',
            'get_distance_range_value_error': 'Пожалуйста, введите число',
            'history_start': 'Выберите дату и команду, чтобы посмотреть найденные отели:',
            'history_clean': 'История поиска пуста',
            'show_history_base_text': 'Команда: {}\n'
                                      'Дата и время: {}',
            'show_history_information_text': '\n\nНазвание отеля: {}\n'
                                             'Адрес: {}\n'
                                             'Расстояние до центра: {}\n'
                                             'Стоимость: {}',
            'text_button_lowprice_hotels': '💲 Дешёвые отели',
            'text_button_hightprice_hotels': '💲💲 Дорогие отели',
            'text_button_bestdeal_hotels': '🧐 Поиск отелей по цене/расположению от центра',
            'text_button_history': '💾 История поиска',
            'text_button_cancel_state': 'Отмена ❌'
        },
        'en_US': {
            'any_state': "You're out of the script",
            'city_founding': '🌆 Select a city from the list:',
            'city_founding_zero': 'In the database Hotels.com there are no cities with this name',
            'city_founding_api_error': 'API error. Try again later',
            'get_city_id_send_name_city': '🌆 City: {}',
            'get_city_id_distance_from_landmark': '💵 Send the minimum price per night ({}):',
            'calendar_check_in': '📆 Select {} check-in',
            'calendar_check_out': '📆 Select {} departure',
            'calendar_results': '🛬 Arrival date: {}\n'
                                '🛫 Departure date: {}\n',
            'calendar_func_end': '💃🕺 Enter the number of adults in the room:',
            'adults_number_func': '🏨🏨🏨 Maximum number of hotels:',
            'asults_number_valid_error': 'Please enter a number',
            'check_data_func_base_info': '\n🛬 Arrival date: {}\n🛫 Departure date: {}'
                                         '\n💃🕺 Number of adults: {}',
            'check_data_distance_from_landmark_text': '\n💵Minimum cost of accommodation per night: {}'
                                                      '\n💵Maximum cost of accommodation per night: {}'
                                                      '\n📍Maximum distance to the center: {}',
            'check_data_func': 'Check the entered data: {}',
            'check_data_func_valid_error': 'Please enter a number',
            'get_answer_check_data_repeat': 'Fill out the questionnaire again',
            'get_answer_check_data_answer_no_distance': '💵 Send the minimum price per night.',
            'show_hotels_func_api_error': 'API error. Try again later',
            'caption_hotel': '🏨 {}\n⭐ Rating: {}\n📫 Address: {}\n'
                             '📍 Distance to the center: {}\n'
                             '💲 Cost per night: {}\n💲💲Cost for the entire period: '
                             '{}\nHotel {} out of {}',
            'show_hotels_func_zero_func': 'There were no hotels with such parameters.',
            'flipper_hotels_close': 'Viewing hotels is closed',
            'get_numbers_photo': 'Required number of photos:',
            'show_photos_zero': 'There are no photos of this hotel.',
            'show_photos_valid_error': 'Please enter a number',
            'base_start': '🌆 Send the bot a city to search for:',
            'get_price_range_price_min': '💵 Send the maximum price per night ({}):',
            'get_price_range_max_distance': '📍 Send the maximum distance to the center ({}):',
            'get_price_range_valid_error': 'Please enter a number',
            'get_distance_range_value_error': 'Please enter a number',
            'history_start': 'Select the date and team to view the hotels found:',
            'history_clean': 'Search history is empty',
            'show_history_base_text': 'Сommand: {}\n'
                                      'Date and time: {}',
            'show_history_information_text': '\n\nName of the hotel: {}\n'
                                             'Address: {}\n'
                                             'Distance to the center: {}\n'
                                             'Cost: {}',
            'text_button_lowprice_hotels': '💲 Cheap hotels',
            'text_button_hightprice_hotels': '💲💲 Expensive hotels',
            'text_button_bestdeal_hotels': '🧐 Search for hotels by price/location from the center',
            'text_button_history': '💾 Search history',
            'text_button_cancel_state': 'Cancel ❌'
        },
        'de_DE': {
            'any_state': 'Sie haben das Skript verlassen',
            'city_founding': '🌆 Wählen Sie eine Stadt aus der Liste aus:',
            'city_founding_zero': 'In der Datenbank Hotels.com es gibt keine Städte mit diesem Namen',
            'city_founding_api_error': 'API-Fehler. Versuchen Sie es später erneut',
            'get_city_id_send_name_city': '🌆 Die Stadt: {}',
            'get_city_id_distance_from_landmark': '💵 Senden Sie den Mindestpreis pro Nacht ({}):',
            'calendar_check_in': '📆 Wählen Sie {} Check-in',
            'calendar_check_out': '📆 Wählen Sie {} Abreise',
            'calendar_results': '🛬 Check-in: {}\n'
                                '🛫 Abreisedatum: {}\n',
            'calendar_func_end': '💃🕺 Bitte geben Sie die Anzahl der Erwachsenen im Zimmer ein:',
            'adults_number_func': '🏨🏨🏨 Maximale Anzahl von Hotels:',
            'asults_number_valid_error': 'Bitte geben Sie eine Nummer ein',
            'check_data_func_base_info': '\n🛬 Check-in: {}\n🛫 Abreisedatum: {}'
                                         '\n💃🕺 Anzahl der gewachsenen: {}',
            'check_data_distance_from_landmark_text': '\n💵Mindestaufenthalt pro Nacht: {}'
                                                      '\n💵Höchstpreis pro Nacht: {}'
                                                      '\n📍Maximale Entfernung zum Zentrum: {}',
            'check_data_func': 'Überprüfen Sie die eingegebenen Daten: {}',
            'check_data_func_valid_error': 'Bitte geben Sie eine Nummer ein',
            'get_answer_check_data_repeat': 'Füllen Sie den Fragebogen erneut aus',
            'get_answer_check_data_answer_no_distance': '💵 Senden Sie den Mindestpreis pro Nacht.',
            'show_hotels_func_api_error': 'API-Fehler. Versuchen Sie es später erneut',
            'caption_hotel': '🏨 {}\n⭐ Bewertung: {}\n📫 Die Adresse: {}\n'
                             '📍 Entfernung zum Zentrum: {}\n'
                             '💲 Kosten pro Nacht: {}\n💲💲Kosten für den gesamten Zeitraum: '
                             '{}\nDas Hotel {} von {}',
            'show_hotels_func_zero_func': 'Es gibt keine Hotels mit solchen Parametern.',
            'flipper_hotels_close': 'Die Hotelansicht ist geschlossen',
            'get_numbers_photo': 'Erforderliche Anzahl von Fotos:',
            'show_photos_zero': 'Es gibt keine Fotos von diesem Hotel.',
            'show_photos_valid_error': 'Sie müssen eine Zahl eingeben',
            'base_start': '🌆 Senden Sie dem Bot eine Stadt für die Suche:',
            'get_price_range_price_min': '💵 Senden Sie den Höchstpreis pro Nacht ({}):',
            'get_price_range_max_distance': '📍 Senden Sie die maximale Entfernung zum Zentrum ({}):',
            'get_price_range_valid_error': 'Bitte geben Sie eine Nummer ein',
            'get_distance_range_value_error': 'Bitte geben Sie eine Nummer ein',
            'history_start': 'Wählen Sie ein Datum und ein Team aus, um die gefundenen Hotels zu sehen:',
            'history_clean': 'Der Suchverlauf ist leer',
            'show_history_base_text': 'Befehl: {}\n'
                                      'Datum und Uhrzeit: {}',
            'show_history_information_text': '\n\nName des Hotels: {}\n'
                                             'Die Adresse: {}\n'
                                             'Entfernung zum Zentrum: {}\n'
                                             'Wert: {}',
            'text_button_lowprice_hotels': '💲 Günstige Hotels',
            'text_button_hightprice_hotels': '💲💲 Teure Hotels',
            'text_button_bestdeal_hotels': '🧐 Suche nach Hotels nach Preis/Lage vom Zentrum',
            'text_button_history': '💾 Suchverlauf',
            'text_button_cancel_state': 'Annullierung ❌'
        },
        'fr_FR': {
            'any_state': 'Vous êtes sorti du script',
            'city_founding': '🌆 Sélectionnez une ville dans la liste:',
            'city_founding_zero': 'Dans la base de données Hotels.com pas de villes avec ce nom',
            'city_founding_api_error': 'Erreur API. Réessayez ultérieurement',
            'get_city_id_send_name_city': '🌆 Ville: {}',
            'get_city_id_distance_from_landmark': '💵 Отправьте минимальную цену за ночь ({}):',
            'calendar_check_in': "📆 Choisissez votre {} d'arrivée",
            'calendar_check_out': "📆 Choisissez votre {} de départ",
            'calendar_results': "🛬 Date d'arrivée: {}\n"
                                "🛫 Date de départ: {}\n",
            'calendar_func_end': '💃🕺 Envoyer le prix minimum par nuit:',
            'adults_number_func': "🏨🏨🏨 Nombre maximum d'Hôtels:",
            'asults_number_valid_error': 'Veuillez entrer le numéro',
            'check_data_func_base_info': "\n🛬 Date d'arrivée: {}\n🛫 Date de départ: {}"
                                         '\n💃🕺 Nombre de blessés: {}',
            'check_data_distance_from_landmark_text': '\n💵Tarif minimum par nuit: {}'
                                                      '\n💵Le tarif maximum par nuit: {}'
                                                      '\n📍Distance maximale au centre: {}',
            'check_data_func': 'Vérifiez les données saisies: {}',
            'check_data_func_valid_error': 'Veuillez entrer le numéro',
            'get_answer_check_data_repeat': 'Remplissez à nouveau le questionnaire',
            'get_answer_check_data_answer_no_distance': '💵 Envoyer le prix minimum par nuit.',
            'show_hotels_func_api_error': 'Erreur API. Réessayez ultérieurement',
            'caption_hotel': '🏨 {}\n⭐️Classement: {}\n📫 Adresse: {}\n'
                             '📍 Distance au centre: {}\n'
                             '💲 Prix par nuit: {}\n💲💲Coût pour toute la période: '
                             '{}\nHôtel {} sur {}',
            'show_hotels_func_zero_func': "Les Hôtels avec de tels paramètres n'ont pas été trouvés.",
            'flipper_hotels_close': 'Voir les Hôtels fermés',
            'get_numbers_photo': 'Nombre de photos requis:',
            'show_photos_zero': "Il n'y a pas de photos de cet hôtel.",
            'show_photos_valid_error': 'Vous devez entrer un nombre',
            'base_start': '🌆 Envoyez un bot à la ville pour la recherche:',
            'get_price_range_price_min': '💵 Envoyez le prix maximum par nuit ({}):',
            'get_price_range_max_distance': '📍 Envoyer la distance maximale au centre ({}):',
            'get_price_range_valid_error': 'Veuillez entrer le numéro',
            'get_distance_range_value_error': 'Veuillez entrer le numéro',
            'history_start': 'Choisissez une date et une commande pour voir les Hôtels trouvés:',
            'history_clean': "L'historique de recherche est vide",
            'show_history_base_text': 'Commande: {}\n'
                                      'Дата и время: {}',
            'show_history_information_text': '\n\nDate et heure: {}\n'
                                             'Adresse: {}\n'
                                             'Distance au centre: {}\n'
                                             'Coût: {}',
            'text_button_lowprice_hotels': '💲 Hôtels bon marché',
            'text_button_hightprice_hotels': '💲💲 Hôtels de luxe',
            'text_button_bestdeal_hotels': '🧐 Trouver des Hôtels par prix/emplacement du centre',
            'text_button_history': '💾 Historique de la recherche',
            'text_button_cancel_state': 'Annulation ❌'
        },
        'it_IT': {
            'any_state': 'Sei fuori dallo script',
            'city_founding': "🌆 Seleziona una città dall'elenco:",
            'city_founding_zero': 'Nel database Hotels.com nessuna città con quel nome',
            'city_founding_api_error': 'Errore API. Riprova più tardi',
            'get_city_id_send_name_city': '🌆 Città: {}',
            'get_city_id_distance_from_landmark': '💵 Invia un prezzo minimo per notte ({}):',
            'calendar_check_in': "📆 Scegli la {} di arrivo",
            'calendar_check_out': "📆 Scegli una {} di partenza",
            'calendar_results': "🛬 Data di arrivo: {}\n"
                                "🛫 Data della partenza: {}\n",
            'calendar_func_end': '💃🕺 Inserisci il numero di adulti per camera:',
            'adults_number_func': '🏨🏨🏨 Numero massimo di hotel:',
            'asults_number_valid_error': 'Si prega di inserire il numero',
            'check_data_func_base_info': '\n🛬 Data di arrivo: {}\n🛫 Data della partenza: {}'
                                         '\n💃🕺 Numero di adulti: {}',
            'check_data_distance_from_landmark_text': '\n💵Prezzo minimo per notte: {}'
                                                      '\n💵Prezzo massimo per notte: {}'
                                                      '\n📍Distanza massima dal centro: {}',
            'check_data_func': 'Controlla i dati inseriti: {}',
            'check_data_func_valid_error': 'Si prega di inserire il numero',
            'get_answer_check_data_repeat': 'Compila nuovamente il questionario',
            'get_answer_check_data_answer_no_distance': '💵 Invia un prezzo minimo per notte.',
            'show_hotels_func_api_error': 'Errore API. Riprova più tardi',
            'caption_hotel': '🏨 {}\n⭐️Rating: {}\n📫 Indirizzo: {}\n'
                             '📍 Distanza dal centro: {}\n'
                             "💲 Costo per notte: {}\n💲💲Costo per l'intero periodo: "
                             '{}\nHotel {} di {}',
            'show_hotels_func_zero_func': 'Hotel con tali parametri non sono stati trovati.',
            'flipper_hotels_close': 'Visualizza Hotel chiuso',
            'get_numbers_photo': 'Numero richiesto di foto:',
            'show_photos_zero': 'Non ci sono foto di questo hotel.',
            'show_photos_valid_error': 'Необходимо ввести число',
            'base_start': '🌆 È necessario inserire un numero:',
            'get_price_range_price_min': '💵 Invia il prezzo massimo per notte ({}):',
            'get_price_range_max_distance': '📍 Invia la distanza massima dal centro ({}):',
            'get_price_range_valid_error': 'Si prega di inserire il numero',
            'get_distance_range_value_error': 'Si prega di inserire il numero',
            'history_start': 'Scegli una data e una squadra per vedere gli hotel trovati:',
            'history_clean': "La cronologia delle ricerche è vuota",
            'show_history_base_text': 'Comando: {}\n'
                                      'Data e ora: {}',
            'show_history_information_text': "\n\nNome dell'hotel: {}\n"
                                             'Indirizzo: {}\n'
                                             'Distanza dal centro: {}\n'
                                             'Costo: {}',
            'text_button_lowprice_hotels': '💲 Hotel economici',
            'text_button_hightprice_hotels': '💲💲 Hotel costosi',
            'text_button_bestdeal_hotels': '🧐 Cerca Hotel per Prezzo/posizione dal centro',
            'text_button_history': '💾 Cronologia delle ricerche',
            'text_button_cancel_state': 'Cancellazione ❌'
        },
        'es_ES': {
            'any_state': 'Estás fuera del guión',
            'city_founding': '🌆 Seleccione una ciudad de la lista:',
            'city_founding_zero': 'En la base de datos Hotels.com no hay ciudades con ese nombre',
            'city_founding_api_error': 'Error de API. Inténtelo de nuevo más tarde',
            'get_city_id_send_name_city': '🌆 Ciudad: {}',
            'get_city_id_distance_from_landmark': '💵 Envíe el precio mínimo por noche ({}):',
            'calendar_check_in': "📆 Seleccione {} entrada",
            'calendar_check_out': "📆 Seleccione {} salida",
            'calendar_results': "🛬 Fecha de llegada: {}\n"
                                "🛫 Fecha de salida: {}\n",
            'calendar_func_end': '💃🕺 Introduzca el número de adultos en la habitación:',
            'adults_number_func': '🏨🏨🏨 Número máximo de hoteles:',
            'asults_number_valid_error': 'Por favor, introduzca el número',
            'check_data_func_base_info': '\n🛬 Fecha de llegada: {}\n🛫 Fecha de salida: {}'
                                         '\n💃🕺 Número de ponderados: {}',
            'check_data_distance_from_landmark_text': '\n💵Tarifa mínima por noche: {}'
                                                      '\n💵Tarifa máxima por noche: {}'
                                                      '\n📍Distancia máxima al centro: {}',
            'check_data_func': 'Verifique los datos ingresados: {}',
            'check_data_func_valid_error': 'Por favor, introduzca el número',
            'get_answer_check_data_repeat': 'Rellene el cuestionario de nuevo',
            'get_answer_check_data_answer_no_distance': '💵 Envíe el precio mínimo por noche.',
            'show_hotels_func_api_error': 'Error de API. Inténtelo de nuevo más tarde',
            'caption_hotel': '🏨 {}\n⭐️Rating: {}\n📫 Dirección: {}\n'
                             '📍 Distancia al centro: {}\n'
                             '💲 Costo por noche: {}\n💲💲Costo para todo el período: '
                             '{}\nHotel {} de {}',
            'show_hotels_func_zero_func': 'Hoteles con tales parámetros no se encontraron.',
            'flipper_hotels_close': 'Ver hoteles cerrados',
            'get_numbers_photo': 'Número requerido de fotos:',
            'show_photos_zero': 'No hay fotos de este hotel.',
            'show_photos_valid_error': 'Debe introducir un número',
            'base_start': '🌆 Enviar un bot ciudad para buscar:',
            'get_price_range_price_min': '💵 Envíe el precio máximo por noche ({}):',
            'get_price_range_max_distance': '📍 Enviar la distancia máxima al centro ({}):',
            'get_price_range_valid_error': 'Por favor, introduzca el número',
            'get_distance_range_value_error': 'Por favor, introduzca el número',
            'history_start': 'Seleccione una fecha y un equipo para ver los hoteles encontrados:',
            'history_clean': "El historial de búsqueda está vacío",
            'show_history_base_text': 'Comando: {}\n'
                                      'Fecha y hora: {}',
            'show_history_information_text': '\n\nNombre del hotel: {}\n'
                                             'Dirección: {}\n'
                                             'Distancia al centro: {}\n'
                                             'Costo: {}',
            'text_button_lowprice_hotels': '💲 Hoteles baratos',
            'text_button_hightprice_hotels': '💲💲 Hoteles caros',
            'text_button_bestdeal_hotels': '🧐 Buscar hoteles por precio/ubicación desde el centro',
            'text_button_history': '💾 Historial de búsqueda',
            'text_button_cancel_state': 'Cancelación ❌'
        }
    }
    text = multilingual_messages[locale][key].format(*args)
    return text

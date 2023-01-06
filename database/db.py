import sqlite3 as sq
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        with self.connection:
            self.cursor.executescript("""
                            CREATE TABLE IF NOT EXISTS language_and_currency (
                                user_id INTEGER PRIMARY KEY,
                                lang TEXT NOT NULL, 
                                currency TEXT NOT NULL);
                            CREATE TABLE IF NOT EXISTS search_history (
                                user_id INTEGER NOT NULL,
                                hotel_id INTEGER NOT NULL,
                                command TEXT NOT NULL,
                                date_time TEXT NOT NULL);
                            CREATE TABLE IF NOT EXISTS information_about_hotels (
                                hotel_id INTEGER NOT NULL,
                                hotel_name TEXT NOT NULL,
                                address TEXT NOT NULL,
                                distance_from_landmark REAL NOT NULL,
                                current_price REAL NOT NULL
                            )
                            """)

    def update_lang_currency_user(self, user_id, lang, currency):
        with self.connection:
            self.cursor.execute("INSERT OR IGNORE INTO language_and_currency VALUES (?, ?, ?)",
                                (user_id, lang, currency))
            self.cursor.execute("UPDATE language_and_currency SET lang = ?, currency=? WHERE user_id=?",
                                (lang, currency, user_id))

    def select_lang_currency_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT lang, currency FROM language_and_currency WHERE user_id=?",
                                       (user_id,)).fetchone()

    def select_locale_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT lang FROM language_and_currency WHERE user_id=?",
                                       (user_id,)).fetchone()
    def update_search_history(self, user_id, command, hotels_id_list):
        data_to_insert = []
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for hotel_id in hotels_id_list:
            data_to_insert.append((user_id, hotel_id, command, date_time))

        with self.connection:
            return self.cursor.executemany("INSERT INTO search_history VALUES (?,?,?,?)", (data_to_insert))

    def update_information_about_hotel(self, hotels_list):
        data = list(map(lambda hotel_info: (hotel_info['hotel_id'], hotel_info['name'], hotel_info['address'],
                                            hotel_info['distance_landmark'], hotel_info['price']), hotels_list))
        with self.connection:
            return self.cursor.executemany("INSERT INTO information_about_hotels VALUES (?,?,?,?,?)", (data))

    def select_command_date_time_by_user_id(self, user_id):
        with self.connection as con:
            con.row_factory = sq.Row
            return con.execute("SELECT * FROM search_history WHERE user_id=?", (user_id,))

    def select_hotel_information_by_hotel_id(self, hotel_ids):
        print(hotel_ids)
        print(type(hotel_ids))
        with self.connection as con:
            con.row_factory = sq.Row
            for hotel_id in hotel_ids:
                yield con.execute("SELECT * FROM information_about_hotels WHERE hotel_id=?", (hotel_id,))


from telebot.types import Message

from database.db import Database
from keyboards.reply import reply_markups
from loader import bot
from states.start_states import LangCurrencyStates


db = Database('database/database.db')


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.set_state(message.from_user.id, LangCurrencyStates.language, message.chat.id)
    bot.send_message(message.from_user.id,
                     '(RU) Выберите язык\n'
                     '(EN) Choose a language\n'
                     '(DE) Wählen Sie die Sprache\n'
                     '(FR) Choisissez la langue\n'
                     '(IT) Scegli la lingua\n'
                     '(ES) Elige el idioma', reply_markup=reply_markups.choose_language_markup())


@bot.message_handler(state=LangCurrencyStates.language)
def get_language(message: Message):
    language_dict = {
        'RU': 'ru_RU',
        'EN': 'en_US',
        'DE': 'de_DE',
        'FR': 'fr_FR',
        'IT': 'it_IT',
        'ES': 'es_ES'
    }
    if message.text in language_dict.keys():
        bot.set_state(message.from_user.id, LangCurrencyStates.currency, message.chat.id)
        bot.send_message(message.from_user.id, 'Выберите валюту:', reply_markup=reply_markups.choose_currency_markup())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['language'] = language_dict[message.text]
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выберите язык из предложенных')


@bot.message_handler(state=LangCurrencyStates.currency)
def get_currency(message: Message):
    currency_list = ['RUB', 'EUR', 'USD', 'GBP', 'KZT', 'UAH', 'CNY', 'JPY']
    if message.text in currency_list:
        currency = message.text
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            language = data['language']
        bot.delete_state(message.from_user.id, message.chat.id)
        db.update_lang_currency_user(message.from_user.id, language, currency)
        bot.send_message(message.from_user.id, 'Язык и валюта выбраны!',
                         reply_markup=reply_markups.base_reply_markup(language))
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выберите валюту из предложенных')

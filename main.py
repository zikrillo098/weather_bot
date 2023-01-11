import requests
from bs4 import BeautifulSoup
import sqlite3
from telebot import TeleBot
from telebot.types import Message
from datetime import datetime

bot = TeleBot('5934207198:AAFUlnVU_68qzF5-GnvxOcwbmfcg6UyZAgs')


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f'Assalomu aleykum {first_name}')
    give_me_weather(message)


def give_me_weather(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введите город в котором хотите узнать погоду: ')
    bot.register_next_step_handler(msg, weather)


def weather(message):
    db = sqlite3.connect('weather.db')
    cursor = db.cursor()
    chat_id = message.chat.id
    paremeters = {
        'appid': 'f6e79d872fe9cd05394ce72d1a8a6227',
        'units': 'metric',
        'lang': 'ru'
    }
    city = message.text
    paremeters['q'] = city
    try:
        data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=paremeters).json()
        temp = data['main']['temp']
        status = data['weather'][0]['description']
        wind = data['wind']['speed']
        sunrise = datetime.utcfromtimestamp(int(data['sys']['sunrise']) + int(data['timezone'])).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(int(data['sys']['sunset']) + int(data['timezone'])).strftime('%H:%M:%S')

        text = f'''В городе {city} сейчас {status}
Температура: {temp} °C
Скорость ветра: {wind} м/с
Восход: {sunrise}
Закат: {sunset}'''
        bot.send_message(chat_id, text)
        cursor.execute('''
            INSERT INTO weather(city, temp, status, wind, sunrise, sunset) VALUES
            (?, ?, ?, ?, ?, ?);
            ''', (city, temp, status, wind, sunrise, sunset))
        db.commit()
    except Exception as e:
        print(f'''Ваша {city} введена не правильно''')
    give_me_weather(message)


bot.polling(none_stop=True)

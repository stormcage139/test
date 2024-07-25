import telebot
from telebot import types
import webbrowser
import sqlite3
import requests, json
from bs4 import BeautifulSoup as BS

# Use your telegtrambotAPI
bot_api = open("telebotapi").readline()
bot = telebot.TeleBot(bot_api)
weather_api = "9f09b90a765e2eb2b66de333e081e988"

url = "https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BB%D1%83%D0%B3%D0%B5,_%D0%9A%D0%B0%D0%BB%D1%83%D0%B6%D1%81%D0%BA%D0%B0%D1%8F_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C"
r = requests.get(url)
html = BS(r.text, 'html.parser')
t1 = html.find(class_='round-5').find(id='forecastShort-content').text
t = t1.split(",")

authorized = False
admin_mode = False
admin_secure = ["admin", "123"]
last_start_usage = 0


def authorized_error(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("/Авторизация")
    btn2 = types.KeyboardButton("/Регистрация")
    # Кнопки Панели(не чата)
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f"Авторизируйтесь путем написания /Авторизация или нажмите на кнопку",
                     reply_markup=markup)


@bot.message_handler(commands=["start"])
def start_button(message):
    global authorized
    global admin_mode
    conn = sqlite3.connect("storm_bot.sql")
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    # Создание sqlite базы данных
    tony_stark = open("./1.jpg", "rb")
    markup = types.InlineKeyboardMarkup()
    # Маркап кнопок под сообщ
    markup2 = types.ReplyKeyboardMarkup()
    btn = types.InlineKeyboardButton("Исходный код бота",
                                     url="https://github.com/stormcage139/test/blob/master/test1.py")
    btn1 = types.InlineKeyboardButton("Элемент гайда по которому сделаны кнопки",
                                      url="https://youtu.be/RpiWnPNTeww?si=cY81QoEYM6rpc1b4&t=996")
    btn_sign = types.InlineKeyboardButton("Авторизация", callback_data="signin")
    btn_register = types.InlineKeyboardButton("Регистрация", callback_data="signup")
    # Создание кнопок для внедрения в маркап под сообщением
    btn2 = types.KeyboardButton("/Регистрация")
    btn3 = types.KeyboardButton("/Авторизация")
    btn4 = types.KeyboardButton("/AdminPanel")

    markup.row(btn, btn1)
    markup.row(btn_sign, btn_register)
    markup2.row(btn2, btn3)
    markup2.row(btn4)
    bot.send_photo(message.chat.id, tony_stark, reply_markup=markup2)

    bot.send_message(message.chat.id, f"Данный бот создан для изучение библиотеки telebot,так что скудный "
                                      "функцинал прошу не "
                                      f"осуждать\nАвтори"
                                      f"зирован - {'да' if authorized else 'нет'}\nРежим "
                                      f"Админа - {'да' if admin_mode else 'нет'}",
                     reply_markup=markup)


@bot.message_handler(commands=["Регистрация"])
def register(message):
    bot.send_message(message.chat.id, "Для продолжения введи Имя Пользователя")
    bot.register_next_step_handler(message, reg_user_name)


def reg_user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, "Для продолжения введи пароль")
    bot.register_next_step_handler(message, reg_user_pass, name)


#     вся функция посвящена получению имени пользователя,потом перенаправляет на функцию получения пароля


def reg_user_pass(message, name):
    password = message.text.strip()
    conn = sqlite3.connect("storm_bot.sql")
    cur = conn.cursor()

    cur.execute(f'INSERT INTO users (name, pass) VALUES ("{name}", "{password}")')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Теперь войдите в аккаунт", callback_data="signin"))
    bot.send_message(message.chat.id, "Пользователь зарегестрирован", reply_markup=markup)


#     функция запрашивает пароль,вызвает базу данных,добавляет данные в базу

@bot.message_handler(commands=["Авторизация"])
def signin(message):
    bot.send_message(message.chat.id, "Для продолжения введи Имя Пользователя")
    bot.register_next_step_handler(message, signin_step2)


def signin_step2(message):
    user_say = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль от аккаунта")
    bot.register_next_step_handler(message, signin_step3, user_say)


def signin_step3(message, user_say1):
    user_say = message.text.strip()
    conn = sqlite3.connect("storm_bot.sql")
    cur = conn.cursor()

    cur.execute('SELECT * from users')
    users = cur.fetchall()
    info = ""
    for el in users:
        if el[2] == user_say and el[1] == user_say1:
            bot.send_message(message.chat.id, "Вы авторизованы")
            global authorized
            authorized = True
    cur.close()
    conn.close()


@bot.callback_query_handler(func=lambda call: True)
def users_list(call):
    if call.data == "users":
        conn = sqlite3.connect("storm_bot.sql")
        cur = conn.cursor()

        cur.execute('SELECT * from users')
        users = cur.fetchall()
        info = ""
        for el in users:
            info += f'Имя: {el[1]}, пароль: {el[2]}\n'
        cur.close()
        conn.close()

        bot.send_message(call.message.chat.id, info)
    elif call.data == "qwe":
        admin_author_step1(call.message)
    elif call.data == "signin":
        signin(call.message)
    elif call.data == "signup":
        register(call.message)


@bot.message_handler(commands=["AdminPanel"])
def admin_author_step1(message):
    bot.send_message(message.chat.id, "Введите логин")
    bot.register_next_step_handler(message, admin_author_step2)


def admin_author_step2(*args):
    message = args[0]
    admin_name = message.text.strip()
    bot.send_message(message.chat.id, "Введите Пароль")
    bot.register_next_step_handler(message, admin_author_last, admin_name)


def admin_author_last(*info):
    message = info[0]
    admin_name = info[1]
    global authorized
    global admin_secure
    global admin_mode
    if message.text == admin_secure[1] and admin_name == admin_secure[0]:
        bot.send_message(message.chat.id, "Вы в режиме администратора")
        admin_mode = True
        authorized = True
    else:
        bot.send_message(message.chat.id, "Бан")
        bot.send_message(message.chat.id, f"{message.text}{admin_secure[0]}   {admin_name}{admin_secure[1]}")


@bot.message_handler(commands=["калуга"])
def kaluga_weather(message):
    global t
    r = requests.get("https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BB%D1%83%D0%B3%D0%B5,"
                     "_%D0%9A%D0%B0%D0%BB%D1%83%D0%B6%D1%81%D0%BA%D0%B0%D1%8F_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%"
                     "82%D1%8C")
    html = BS(r.text, 'html.parser')
    t1 = html.find(class_='round-5').find(id='forecastShort-content').text
    t = t1.split(",")
    t[0] = t[0].replace("..", " - ")
    t[3] = t[3].replace("..", " - ")
    a = f"{t[0][:-2]} , {t[2]} , {t[3][:-2]} , {t[5]} , {t[6]}"
    bot.reply_to(message, f'{a}')


@bot.message_handler(commands=["weather"])
def weather_start(message):
    if authorized:
        bot.send_message(message.chat.id, "Напиши название города в котором хочешь узнать погоду")
        bot.register_next_step_handler(message, weather_end)
    else:
        authorized_error(message)


def weather_end(message):
    city = message.text.strip().lower()
    weather_city = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric")
    if weather_city.status_code == 200:
        temperature = json.loads(weather_city.text)
        bot.reply_to(message, f'Сейчас температура: {temperature["main"]["temp"]}')
    else:
        bot.reply_to(message, f'Неверно введен город, повторите попытку')
        bot.register_next_step_handler(message, weather_end)


@bot.message_handler(commands=["hello"])
def start(message):
    if authorized:
        bot.send_message(message.chat.id, f"Привет, {message.from_user.last_name} {message.from_user.first_name}")
    else:
        authorized_error(message)


@bot.message_handler(commands=["a"])
def start_button(message):
    global authorized
    global admin_mode
    authorized = True
    admin_mode = True


# @bot.message_handler(commands=["auto"])
# def signin(message):
#     bot.send_message(message.chat.id, "Скинь фото")
#
#     @bot.message_handler(content_types=["photo"])
#     def photocheck(message2):
#         markup = types.InlineKeyboardMarkup()
#         btn1 = types.InlineKeyboardButton("Вам выдан доступ на сайт с кодом",
#                                           url="https://github.com/stormcage139/test/blob/master/test1.py")
#         markup.row(btn1)
#         bot.reply_to(message2, "ЛЕХЕНДА", reply_markup=markup)


# @bot.callback_query_handler(func=lambda callback: True)
# def callback_mess(callback):
#     if callback.data == "LOL":
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
@bot.message_handler(commands=["dnd"])
def dnd(message):
    global admin_mode
    if admin_mode:
        bot.reply_to(message, "Выгружаю файл смерти")
        dnd_video_meme = open("./dimka.mp4", "rb")
        bot.send_video(message.chat.id, dnd_video_meme)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("Войти в режим админа", callback_data="qwe"))
        bot.send_message(message.chat.id, f"Вы не админ", reply_markup=markup)


# @bot.callback_query_handler(func=lambda cal: True)
# def not_adm_call(cal):
#     if cal.data == "qwe":
#         bot.send_message(cal.message.chat.id, f"лох")
#         admin_author_step1(cal)


@bot.message_handler()
def otvet(message):
    bot.send_message(message.chat.id, "Ебало завали,распизделась хуета")


bot.infinity_polling()

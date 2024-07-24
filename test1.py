import telebot
from telebot import types
import webbrowser
import sqlite3

bot = telebot.TeleBot("7330806602:AAFrWTvYcEaFXeX8eNBQjEqXVPwGjF5kRZY")


@bot.message_handler(commands=["start"])
def start_button(message):
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
    btn = types.InlineKeyboardButton("Исходный код бота",
                                     url="https://github.com/stormcage139/test/blob/master/test1.py")
    btn1 = types.InlineKeyboardButton("Элемент гайда по которому сделаны кнопки",
                                      url="https://youtu.be/RpiWnPNTeww?si=cY81QoEYM6rpc1b4&t=996")
    markup.row(btn, btn1)
    bot.send_photo(message.chat.id, tony_stark)
    bot.send_message(message.chat.id, "Данный бот создан для изучение библиотеки telebot,так что скудный "
                                      "функцинал прошу не осуждать", reply_markup=markup)
    bot.send_message(message.chat.id, "Для продолжения авторизируйтесь или зарегестрируйтесь")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, "Для продолжения введи пароль")
    bot.register_next_step_handler(message, user_pass, name)
#     вся функция посвящена получению имени пользователя,потом перенаправляет на функцию получения пароля


def user_pass(message, name):
    password = message.text.strip()
    conn = sqlite3.connect("storm_bot.sql")
    cur = conn.cursor()

    cur.execute(f'INSERT INTO users (name, pass) VALUES ("{name}", "{password}")')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Список пользователей", callback_data="users"))
    bot.send_message(message.chat.id, "Пользователь зарегестрирован", reply_markup=markup)
#     функция запрашивает пароль,вызвает базу данных,добавляет данные в базу


@bot.callback_query_handler(func=lambda call: True)
def users_list(call):
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


# def onclick(message):
#     if message.text.lower() == "исходный код бота":
#         webbrowser.open("https://github.com/stormcage139/test/blob/master/test1.py")
#     elif message.text == "Элемент гайда по которому сделаны кнопки":
#         webbrowser.open("https://youtu.be/RpiWnPNTeww?si=cY81QoEYM6rpc1b4&t=996")
#     bot.register_next_step_handler(message, onclick)


@bot.message_handler(commands=["hello"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.last_name} {message.from_user.first_name}")


@bot.message_handler(commands=["user"])
def qqq(message):
    bot.send_message(message.chat.id, message)


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
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1) qqe


bot.infinity_polling()

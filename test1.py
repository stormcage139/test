import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot("7330806602:AAFrWTvYcEaFXeX8eNBQjEqXVPwGjF5kRZY")


@bot.message_handler(commands=["start"])
def start_button(message):
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton("Исходный код бота")
    btn1 = types.KeyboardButton("Элемент гайда по которому сделаны кнопки")
    markup.row(btn)
    markup.row(btn1)
    bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=markup)
    bot.register_next_step_handler(message, onclick)


def onclick(message):
    if message.text.lower() == "исходный код бота":
        webbrowser.open("https://github.com/stormcage139/test/blob/master/test1.py")
    elif message.text == "Элемент гайда по которому сделаны кнопки":
        webbrowser.open("https://youtu.be/RpiWnPNTeww?si=cY81QoEYM6rpc1b4&t=996")
    bot.register_next_step_handler(message, onclick)


@bot.message_handler(commands=["site"])
def site(message):
    webbrowser.open("https://github.com/stormcage139/test/blob/master/test1.py")


@bot.message_handler(commands=["hello"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.last_name} {message.from_user.first_name}")


@bot.message_handler(commands=["user"])
def qqq(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=["test"])
def test(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Вам выдан доступ на сайт с кодом",
                                      url="https://github.com/stormcage139/test/blob/master/test1.py")
    btn2 = types.InlineKeyboardButton("Delete", callback_data="LOL")
    markup.row(btn1, btn2)
    markup.row(btn2)
    bot.send_message(message.chat.id, "Ку", reply_markup=markup)


@bot.message_handler(commands=["auto"])
def signin(message):
    bot.send_message(message.chat.id, "Скинь фото")

    @bot.message_handler(content_types=["photo"])
    def photocheck(message2):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Вам выдан доступ на сайт с кодом",
                                          url="https://github.com/stormcage139/test/blob/master/test1.py")
        markup.row(btn1)
        bot.reply_to(message2, "ЛЕХЕНДА", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_mess(callback):
    if callback.data == "LOL":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)


bot.infinity_polling()

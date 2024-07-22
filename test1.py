import telebot
import webbrowser

bot = telebot.TeleBot("7330806602:AAFrWTvYcEaFXeX8eNBQjEqXVPwGjF5kRZY")


@bot.message_handler(commands=["site"])
def site(message):
    webbrowser.open("https://github.com/stormcage139/test/blob/master/test1.py")


@bot.message_handler(commands=["start", "hello"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.last_name} {message.from_user.first_name}")


@bot.message_handler(commands=["user"])
def qqq(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=["auto"])
def qqq(message):
    bot.send_message(message.chat.id, "Скинь фото")

    @bot.message_handler(content_types=["photo"])
    def photocheck(message):
        bot.reply_to(message, "Авторизирован")


bot.infinity_polling()

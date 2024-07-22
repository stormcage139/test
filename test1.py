import telebot

bot = telebot.TeleBot("7330806602:AAFrWTvYcEaFXeX8eNBQjEqXVPwGjF5kRZY")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет")


bot.polling(non_stop=True)
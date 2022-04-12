from time import sleep 
import random 

import telebot
from telebot import types, apihelper

from datatypes import College
from user import User


Token = '2051085927:AAEROawkgOmL4_Y9IAj13r-2o_zOne5GVYE'
apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(Token)


@bot.middleware_handler(update_types=['message'])
def to_lowercase(bot_instance, message):
    message.text = message.text.lower().replace('ё', 'е')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDJRZhdbuNiolM27tU_cRRG91tvb3jugACCgEAAsizygp-fqfRoggXiCEE')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("😊 Список ведущих вузов ")
    item2 = types.KeyboardButton("Инструкция")
    markup.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь вам выбрать ВУЗ."
        .format(message.from_user, bot.get_me()),
        parse_mode='html',
        reply_markup=markup
    )


@bot.message_handler(regexp="😊 список ведущих вузов")
def send_colleges(message):
    colleges = College.load_all()
    for k in range(0, len(colleges), 50):
        answer = '\n'.join(f'{i}. {name}' for i, name in enumerate(colleges[k : k+50], k + 1))
        bot.send_message(message.chat.id, answer)


@bot.message_handler(regexp="инструкция")
def send_colleges(message):
    bot.send_message(message.chat.id, 'И так всё понятно')


@bot.message_handler(content_types=['text'])
def text(message):
    user = User(message.chat.id)
    answer = user.handle_request(message.text)
    bot.send_message(message.chat.id, answer)


bot.polling()

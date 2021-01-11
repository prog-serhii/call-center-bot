from flask import request
from telebot import types

from app import app, bot, db
from .models import UsersPhones, Messages
from .utils import phone_control
from .modules import Actions, Statistic
import config


act = Actions(bot, db, UsersPhones)
stat = Statistic(db, UsersPhones, Messages)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print('test_messagew')
    act.new_user(message)
    act.send_welcome(message)

    stat.command(message.chat.username, 'start')


@bot.callback_query_handler(func=lambda call: True)
def callback_function(call):
    if call.message:

        if call.data == 'new_call' or call.data == 'correct':
            act.get_request(call.message)
            act.send_call_back(call.message)

            stat.inline_key(call.message.chat.username, call.data)

        elif call.data == 'change':
            act.send_input_phone(call.message)

            stat.inline_key(call.message.chat.username, call.data)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_text(message):
    # если ето номер телефона
    phone = phone_control(message.text)
    if phone:
        act.save_change_phone(message, phone)
        act.send_phone_saved(message)

        stat.phone_number(message.chat.username, phone)

    elif message.text == 'Рабочее время ' + u'\U000023F3':
        act.send_timing(message)

        stat.reply_key(message.chat.username, message.text)

    elif message.text == 'Передзвонить ' + u'\U0001F4DE':
        act.request_call_back(message)

        stat.reply_key(message.chat.username, message.text)

    else:
        stat.message(message.chat.username, message.text)


@app.route("/" + config.TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=config.URL + config.TOKEN)
    return "!", 200

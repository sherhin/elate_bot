import os
import apiai
import json
from telegram.ext import Updater
from utils import back_keyboard

DIALOG_FLOW = os.environ.get('DIALOG_FLOW')


def listen_to_me(bot, update):
    request = apiai.ApiAI(DIALOG_FLOW).text_request()  # Токен API к Dialogflow
    request.lang = 'ru'
    request.chat_id = 'ElateBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=back_keyboard())
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я тебя не понял. Может, чаю?',
                         reply_markup=back_keyboard())

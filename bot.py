import logging
import datetime
import sqlite3
import sys
import apiai, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from utils import get_keyboard
from diagoflow import *
from user_profile import *

PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn',
        'password': 'python',
    },
}


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )   


def greet_user(bot,update):
    text = 'Привет! Я твой персональный ассистент по настроению! Что ты хочешь?'
    update.message.reply_text(text, reply_markup=get_keyboard())

    

def main():
    with open('TOKEN.txt') as f:
        token = f.read().strip()

    mybot = Updater(token, request_kwargs=PROXY)
    dp = mybot.dispatcher #реагирование на событие

    profile=ConversationHandler(
    entry_points = [RegexHandler('^(Познакомься со мной!)$',
                     profile_start, pass_user_data=True)],
    states={
        'name':[MessageHandler(Filters.text,profile_get_name,pass_user_data=True)],
        'age':[MessageHandler(Filters.text,profile_get_age,pass_user_data=True)],
        'gender':[RegexHandler('^(Определенно, мужчина|Определенно, женщина|Один из шестидесяти гендеров)$',
        profile_get_gender,pass_user_data=True)],
    },
    fallbacks=[],
    )
    dp.add_handler(profile)
    dp.add_handler(CommandHandler('start', greet_user))#если придет старт, реагируем функцией 
    dp.add_handler(RegexHandler('^(Выслушай меня!)$',
                     listen_to_me,))
    dp.add_handler(MessageHandler(Filters.text,listen_to_me))
    
  


    mybot.start_polling()#бот начинает опрашивать Телеграмм
    mybot.idle()#бот работает пока не скажут прекратить


if __name__ == '__main__':
    main()
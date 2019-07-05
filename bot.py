import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler
from utils import get_keyboard, greet_user, fun_start
from dialogflow import listen_to_me
from send_image import send_cat
from mem import send_mem, send_joke
from db import db
from conversations import profile
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
def main():
    with open('TOKEN.txt') as f:
        token = f.read().strip()

    mybot = Updater(token, request_kwargs=PROXY)
    dp = mybot.dispatcher #реагирование на событие

    dp.add_handler(CommandHandler('start', greet_user))
    
    dp.add_handler(profile)

    dp.add_handler(RegexHandler('^(Котики)$',
                     send_cat))
    dp.add_handler(RegexHandler('^(Мемы)$',
                     send_mem))
    dp.add_handler(RegexHandler('^(Подними мне настроение!)$',
                     fun_start,))
    dp.add_handler(RegexHandler('^(Анекдоты)$',
                     send_joke))
    dp.add_handler(CommandHandler('image',send_cat))
    dp.add_handler(RegexHandler('^(Выслушай меня!)$',
                     listen_to_me,))
    dp.add_handler(MessageHandler(Filters.text,listen_to_me))
    
  


    mybot.start_polling()#бот начинает опрашивать Телеграмм
    mybot.idle()#бот работает пока не скажут прекратить


if __name__ == '__main__':
    main()
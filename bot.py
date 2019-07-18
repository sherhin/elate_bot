import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler,BaseFilter
from utils import fun_start
from dialogflow import listen_to_me
from send_image import send_cat,send_bash
from mem import send_mem, send_joke
from db import db,profile, greet_user
from db import filter_awesome
from search import user_search
from settings import TOKEN_BOT,PROXY


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    ) 

def main():

    mybot = Updater(TOKEN_BOT, request_kwargs=PROXY)
    dp = mybot.dispatcher #реагирование на событие
    
    dp.add_handler(profile)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(RegexHandler('^(Вернуться)$',
                     greet_user))
    dp.add_handler(CommandHandler('search',user_search))

    dp.add_handler(RegexHandler('^(Котики)$',
                     send_cat))
    dp.add_handler(RegexHandler('^(Мемы)$',
                     send_mem))
    dp.add_handler(RegexHandler('^(Подними мне настроение!)$',
                     fun_start,))
    dp.add_handler(RegexHandler('^(Анекдоты)$',
                     send_joke))
    dp.add_handler(RegexHandler('^(Башорг)$',
                     send_bash))
    dp.add_handler(CommandHandler('image',send_cat))
    dp.add_handler(RegexHandler('^(Выслушай меня!)$',
                     listen_to_me,))
    dp.add_handler(MessageHandler(Filters.text,listen_to_me))
    




    mybot.start_polling()#бот начинает опрашивать Телеграмм
    mybot.idle()#бот работает пока не скажут прекратить


if __name__ == '__main__':
    main()
    
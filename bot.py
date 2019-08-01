import logging
import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, BaseFilter
from utils import fun_start, about_me, bot_say_hi
from dialogflow import listen_to_me
from send_to_user import get_image, get_mem, send_cat, send_mem, send_bash, send_joke
from db import db, profile, greet_user, filter_awesome
from search import search, user_search, stop_search


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


TOKEN_BOT = os.environ.get('TOKEN_BOT')


def main():
    mybot = Updater(TOKEN_BOT)

    mybot.job_queue.run_repeating(bot_say_hi, interval=86400)
    mybot.job_queue.run_repeating(get_image, interval=604800)
    mybot.job_queue.run_repeating(get_mem, interval=604800)

    dp = mybot.dispatcher  # реагирование на событие

    dp.add_handler(profile)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(RegexHandler('^(Вернуться)$',
                                greet_user))
    dp.add_handler(CommandHandler('search', user_search))

    dp.add_handler(RegexHandler('^(Котики)$',
                                send_cat))
    dp.add_handler(RegexHandler('^(Мемы)$',
                                send_mem))
    dp.add_handler(RegexHandler('^(Подними мне настроение!)$',
                                fun_start, ))
    dp.add_handler(RegexHandler('^(Анекдоты)$',
                                send_joke))
    dp.add_handler(RegexHandler('^(Башорг)$',
                                send_bash))
    dp.add_handler(RegexHandler('^(Обо мне)$',
                                about_me))
    dp.add_handler(RegexHandler('^(Поболтай со мной!)$',
                                listen_to_me))
    bot_search = ConversationHandler(
        entry_points=[RegexHandler('^(Погугли)$',
                                   search, pass_user_data=True)],
        states={
            'user_search': [RegexHandler('^(Отмена поиска)$', stop_search, pass_user_data=True),
                            MessageHandler(Filters.text, user_search, pass_user_data=True)],
        },
        fallbacks=[],
    )
    dp.add_handler(bot_search)
    dp.add_handler(MessageHandler(Filters.text, listen_to_me))

    mybot.start_polling()  # бот начинает опрашивать Телеграмм
    mybot.idle()  # бот работает пока не скажут прекратить


if __name__ == '__main__':
    main()

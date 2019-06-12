import logging
import apiai, json
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn',
        'password': 'python',
    },
}


logging.basicConfig(format='%(asktime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )   

def greet_user(bot,update):
    text = 'Привет!'
    my_keyboard = ReplyKeyboardMarkup([
        ['Поддержи меня!', 'Выслушай меня!','Подними мне настроение!'],
    ], resize_keyboard=True
    )
    update.message.reply_text(text, reply_markup=my_keyboard)


def listen_to_me(bot,update):
    request = apiai.ApiAI('2d63bff1ad0d48348ea28e6d162409ae').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'ElateBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не понял!')

def main():
    with open('TOKEN.txt') as f:
        token = f.read().strip()

    mybot = Updater(token, request_kwargs=PROXY)
    dp = mybot.dispatcher #реагирование на событие
    dp.add_handler(CommandHandler('start', greet_user))#если придет старт, реагируем функцией 
    dp.add_handler(RegexHandler('^(Выслушай меня!)$',
                     listen_to_me,))
    dp.add_handler(MessageHandler(Filters.text,listen_to_me))

    mybot.start_polling()#бот начинает опрашивать Телеграмм
    mybot.idle()#бот работает пока не скажут прекратить


if __name__ == '__main__':
    main()
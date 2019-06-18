import logging
import datetime
import apiai, json
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

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

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
        ['Поддержи меня!', 'Выслушай меня!','Подними мне настроение!','Познакомься со мной!'],
    ], resize_keyboard=True
    )
    return my_keyboard

def profile_start(bot,update,user_data):
    text = 'Для того, чтобы лучше тебя понимать, нам надо познакомиться поближе. Скажи, как тебя зовут?'
    update.message.reply_text(text,reply_markup=ReplyKeyboardRemove())
    return "name"

def profile_get_name(bot,update,user_data):
    user_name=update.message.text
    user_data['profile_name']=user_name
    text = f'Оке,{user_name}, сколько тебе лет?'
    update.message.reply_text(text)

    return'age'

def profile_get_age(bot,update,user_data):
    user_age = update.message.text
    user_data['profile_age']=user_age
    update.message.reply_text(f'{user_age} - прекрасный возраст!')
    reply_keyboard=[['Определенно, мужчина','Определенно, женщина','Один из шестидесяти гендеров']]
    update.message.reply_text(text='А ты мальчик, девочка или пока не определился?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    return'gender'

def profile_get_gender(bot,update,user_data):
    if update.message.text=='Определенно, мужчина':
        user_gender='male'
    elif update.message.text=='Определенно, женщина':
        user_gender='female'
    else:
        user_gender=None
    user_data['profile_gender']=user_gender
    update.message.reply_text(f'Я запомнил ;-) ')
    update.message.reply_text(f'Спасибо за ответы! Теперь мы стали чуточку ближе) ')
    return greet_user(bot,update)

    
    

def listen_to_me(bot,update):
    request = apiai.ApiAI('2d63bff1ad0d48348ea28e6d162409ae').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'ElateBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
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

    mybot.start_polling()#бот начинает опрашивать Телеграмм
    mybot.idle()#бот работает пока не скажут прекратить


if __name__ == '__main__':
    main()
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from utils import greet_user
from db import db, get_or_create_user

def profile_start(bot,update,user_data):
    text = 'Для того, чтобы лучше тебя понимать, нам надо познакомиться поближе. Скажи, как тебя зовут?'
    update.message.reply_text(text,reply_markup=ReplyKeyboardRemove())
    return 'name'

def profile_get_name(bot,update,user_data):
    user_data=get_or_create_user(db, update.effective_user, update.message)
    profile_name=update.message.text
    db.users.update_one({'_id':user_data['_id']},
     {'$set':{'profile_name':profile_name}}
     )
    text = f'Оке, сколько тебе лет?'
    update.message.reply_text(text)
    return'age'

def profile_get_age(bot,update,user_data):
    user_data=get_or_create_user(db, update.effective_user, update.message)
    user_age = update.message.text
    db.users.update_one({'_id':user_data['_id']},
     {'$set':{'profile_age':user_age}}
     )
    reply_keyboard=[['Определенно, мужчина','Определенно, женщина','Один из шестидесяти гендеров']]
    update.message.reply_text(text='А ты мальчик, девочка или пока не определился?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    return'gender'

def profile_get_gender(bot,update,user_data):
    user_data=get_or_create_user(db, update.effective_user, update.message)
    if update.message.text=='Определенно, мужчина':
        user_gender='male'
    elif update.message.text=='Определенно, женщина':
        user_gender='female'
    else:
        user_gender=None
    db.users.update_one({'_id':user_data['_id']},
     {'$set':{'profile_gender':user_gender}}
     )
    update.message.reply_text(f'Я запомнил ;-) ')
    update.message.reply_text(f'Спасибо за ответы! Теперь мы стали чуточку ближе) ')
    return greet_user(bot,update)

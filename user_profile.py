from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import sqlite3
from utils import greet_user
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

'''(def create_profile():'''
'''elate_db=sqlite3.connect('elate_db')'''
'''cursor=elate_db.cursor()'''
'''cursor.execute((CREATE TABLE users(user_id,user_name,user_age,user_gender))'''
'''cursor.execute(""INSERT INTO users'''
'''VALUES ('1', '?', '?','''
'''?')"",profile(states['name']),profile(states['age']),profile(states['gender'])'''
''')'''
'''elate_db.commit()
return greet_user(bot,update))'''

    
    
from pymongo import MongoClient
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler, BaseFilter
from utils import get_keyboard, profile_keyboard


db = MongoClient(settings.MONGO_LINK)[settings.MONGO_DB]

def get_user(db,effective_user,message):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        return False
    else:
        return True

    
class FilterAwesome (BaseFilter):
    def filter(self,message):
        user=message.from_user
        db_user=get_user(db,user,message)
        return db_user


        

filter_awesome=FilterAwesome()


        


def create_user(db, effective_user, message,user_data):
    db_user = {
        "user_id": effective_user.id,
        "first_name": effective_user.first_name,
        "last_name": effective_user.last_name,
        "username": effective_user.username,
        "chat_id": message.chat.id,
        "profile_name":user_data['name'],
        "profile_age":user_data['age'],
        "profile_gender":user_data['gender'],
        }
    db.users.insert_one(db_user)
    return db_user

def profile_start(bot,update):
    text = 'Привет! Я твой персональный ассистент по настроению! Я еще маленький и глупый, но благодаря тебе я стану лучше. Нам надо познакомиться поближе. Скажи, как тебя зовут?'
    update.message.reply_text(text,reply_markup=ReplyKeyboardRemove())
    return 'name'


def profile_get_name(bot,update,user_data):
    user_data['name']=update.message.text
    text = f'Оке, сколько тебе лет?'
    update.message.reply_text(text)
    return'age'

def profile_get_age(bot,update,user_data):
    user_data['age'] = update.message.text
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
    user_data['gender']=user_gender
    update.message.reply_text(f'Я запомнил ;-) ')
    update.message.reply_text(f'Спасибо за ответы! Теперь мы стали чуточку ближе) ')
    create_user(db,update.effective_user,update.message,user_data)



profile=ConversationHandler(
    entry_points = [CommandHandler('profile',profile_start)],
    states={
        'name':[MessageHandler(Filters.text,profile_get_name,pass_user_data=True)],
        'age':[MessageHandler(Filters.text,profile_get_age,pass_user_data=True)],
        'gender':[RegexHandler('^(Определенно, мужчина|Определенно, женщина|Один из шестидесяти гендеров)$',
        profile_get_gender,pass_user_data=True)],
    },
    fallbacks=[],
)
def greet_user(bot,update,db_user):
    if db_user:
        user_name=user['profile_name']
        text = f'Привет,{user_name}! Я рад тебя видеть! Чем я могу помочь тебе сегодня?'
        update.message.reply_text(text, reply_markup=get_keyboard())


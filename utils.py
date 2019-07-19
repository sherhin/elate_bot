from telegram import ReplyKeyboardMarkup, KeyboardButton
from db import db, get_user


def fun_keyboard():
    fun_keyboard = ReplyKeyboardMarkup([
        ['Котики'],[ 'Мемы'],['Анекдоты'],['Башорг'],
        ['Вернуться']]
    , resize_keyboard=True
    )
    return fun_keyboard


def back_keyboard():
    back_keyboard=ReplyKeyboardMarkup([
        ['Вернуться']]
    , resize_keyboard=True
    )
    return back_keyboard


def fun_start(bot,update):
    
    text = 'Как мне тебя развлечь?'
    update.message.reply_text(text, reply_markup=fun_keyboard())

def about_me(bot,update):
    with open ('about_me.txt','r',encoding='utf8')as f:
        text=f.readlines()
    for sentence in text:
        update.message.reply_text(sentence,reply_markup=back_keyboard())


def bot_say_hi(bot,job):
    users=db.users.find({'chat_id': {'$exists':True}})
    for user in users:
        user_chat_id=user['chat_id']
        user_profile_name=user['profile_name']
        bot.sendMessage(chat_id=user_chat_id,text=f'Пссс, {user_profile_name}! Не хочешь немного развлечься?',reply_markup=fun_keyboard())
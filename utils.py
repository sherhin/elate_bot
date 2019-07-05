from telegram import ReplyKeyboardMarkup, KeyboardButton
from db import db, get_or_create_user


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
        ['Поддержи меня!'],[ 'Выслушай меня!'],['Подними мне настроение!','Познакомься со мной!']]
    , resize_keyboard=True
    )
    return my_keyboard


def greet_user(bot,update):
    user_data=get_or_create_user(db, update.effective_user, update.message)
    text = 'Привет! Я твой персональный ассистент по настроению! Что ты хочешь?'
    update.message.reply_text(text, reply_markup=get_keyboard())


def fun_keyboard():
    fun_keyboard = ReplyKeyboardMarkup([
        ['Котики'],[ 'Мемы'],['Анекдоты']]
    , resize_keyboard=True
    )
    return fun_keyboard

def fun_start(bot,update):
    user_data=get_or_create_user(db, update.effective_user, update.message)
    text = 'Как мне тебя развлечь?'
    update.message.reply_text(text, reply_markup=fun_keyboard())
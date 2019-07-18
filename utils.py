from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
        ['Поддержи меня!'],[ 'Выслушай меня!'],['Подними мне настроение!']]
    , resize_keyboard=True
    )
    return my_keyboard

def profile_keyboard():
    profile_keyboard=ReplyKeyboardMarkup([
        ['Познакомься со мной!']]
    , resize_keyboard=True
    )
    return profile_keyboard


def fun_keyboard():
    fun_keyboard = ReplyKeyboardMarkup([
        ['Котики'],[ 'Мемы'],['Анекдоты'],['Башорг'],
        ['Вернуться']]
    , resize_keyboard=True
    )
    return fun_keyboard

def back_keyboard():
    fun_keyboard = ReplyKeyboardMarkup([
        ['Котики'],[ 'Мемы'],['Анекдоты'],['Башорг'],['Вернуться']]
    , resize_keyboard=True
    )
    return back_keyboard


def fun_start(bot,update):
    
    text = 'Как мне тебя развлечь?'
    update.message.reply_text(text, reply_markup=fun_keyboard())


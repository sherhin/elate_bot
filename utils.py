from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
        ['Поддержи меня!', 'Выслушай меня!','Подними мне настроение!','Познакомься со мной!'],
    ], resize_keyboard=True
    )
    return my_keyboard


def greet_user(bot,update):
    text = 'Привет! Я твой персональный ассистент по настроению! Что ты хочешь?'
    update.message.reply_text(text, reply_markup=get_keyboard())

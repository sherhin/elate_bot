from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
        ['Поддержи меня!', 'Выслушай меня!','Подними мне настроение!','Познакомься со мной!'],
    ], resize_keyboard=True
    )
    return my_keyboard
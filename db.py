from pymongo import MongoClient
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, BaseFilter

MONGO_LINK=os.environ.get('MONGO_LINK')
MONGO_DB=os.environ.get('MONGO_DB')
db = MongoClient(MONGO_LINK)[MONGO_DB]


def get_user(db, effective_user, message):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        return False
    if user:
        return user


class FilterAwesome(BaseFilter):
    def filter(self, message):
        user = message.from_user
        db_user = get_user(db, user, message)
        if not db_user:
            return True


filter_awesome = FilterAwesome()


def create_user(db, effective_user, message, user_data):
    user = {
        "user_id": effective_user.id,
        "first_name": effective_user.first_name,
        "last_name": effective_user.last_name,
        "username": effective_user.username,
        "chat_id": message.chat.id,
        "profile_name": user_data['name'],
        "profile_age": user_data['age'],
        "profile_gender": user_data['gender'],
    }
    db.users.insert_one(user)
    return user


def profile_start(bot, update):
    text = 'Привет! Меня зовут Эляша и я твой персональный ассистент для поднятия настроения. Я еще маленький и глупый, но благодаря тебе я стану лучше.Скажи, как тебя зовут?'
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return 'name'


def profile_get_name(bot, update, user_data):
    user_data['name'] = update.message.text
    text = f'Оке, сколько тебе лет?'
    update.message.reply_text(text)
    return 'age'


def profile_get_age(bot, update, user_data):
    user_data['age'] = update.message.text
    reply_keyboard = [['Определенно, мужчина', 'Определенно, женщина', 'Один из шестидесяти гендеров']]
    update.message.reply_text(text='А ты мальчик, девочка или пока не определился?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 'gender'


def profile_get_gender(bot, update, user_data):
    if update.message.text == 'Определенно, мужчина':
        user_gender = 'male'
    elif update.message.text == 'Определенно, женщина':
        user_gender = 'female'
    else:
        user_gender = None
    user_data['gender'] = user_gender
    update.message.reply_text(f'Я запомнил ;-) ')
    update.message.reply_text(f'Спасибо за ответы! Теперь мы стали чуточку ближе) ')
    create_user(db, update.effective_user, update.message, user_data)
    return greet_user(bot, update)


profile = ConversationHandler(
    entry_points=[MessageHandler(filter_awesome, profile_start)],
    states={
        'name': [MessageHandler(Filters.text, profile_get_name, pass_user_data=True)],
        'age': [MessageHandler(Filters.text, profile_get_age, pass_user_data=True)],
        'gender': [RegexHandler('^(Определенно, мужчина|Определенно, женщина|Один из шестидесяти гендеров)$',
                                profile_get_gender, pass_user_data=True)],
    },
    fallbacks=[],
)


def start_keyboard():
    start_keyboard = ReplyKeyboardMarkup([
        ['Погугли'], ['Поболтай со мной'], ['Подними мне настроение!'], ['Обо мне']]
        , resize_keyboard=True
    )
    return start_keyboard


def greet_user(bot, update):
    user = get_user(db, update.effective_user, update.message)
    if user == False:
        text = 'Привет! Я твой персональный ассистент по настроению! Я еще маленький и глупый, но благодаря тебе я стану лучше.'
        update.message.reply_text(text)
        profile_start(bot, update)
    user_name = user['profile_name']
    text = f'Привет,{user_name}! Я рад тебя видеть! Чем я могу помочь тебе сегодня?'
    update.message.reply_text(text, reply_markup=start_keyboard())

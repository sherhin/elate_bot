from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, BaseFilter
from db import db, profile_get_name, profile_get_age, profile_get_gender,profile_start, get_user


class FilterAwesome(BaseFilter):
    def filter(self, message):
        user = message.from_user
        db_user = get_user(db, user, message)
        if not db_user:
            return True


filter_awesome = FilterAwesome()



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

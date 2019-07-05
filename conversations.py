from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler
from user_profile import profile_start, profile_get_name, profile_get_age, profile_get_gender

profile=ConversationHandler(
    entry_points = [RegexHandler('^(Познакомься со мной!)$',
                     profile_start,pass_user_data=True)],
    states={
        'name':[MessageHandler(Filters.text,profile_get_name,pass_user_data=True)],
        'age':[MessageHandler(Filters.text,profile_get_age,pass_user_data=True)],
        'gender':[RegexHandler('^(Определенно, мужчина|Определенно, женщина|Один из шестидесяти гендеров)$',
        profile_get_gender,pass_user_data=True)],
    },
    fallbacks=[],
    )

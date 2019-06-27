from telegram.ext import Updater,CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler

profile=ConversationHandler(
    entry_points = [RegexHandler('^(Познакомься со мной!)$',
                     profile_start, pass_user_data=True)],
    states={
        'name':[MessageHandler(Filters.text,profile_get_name,pass_user_data=True)],
        'age':[MessageHandler(Filters.text,profile_get_age,pass_user_data=True)],
        'gender':[RegexHandler('^(Определенно, мужчина|Определенно, женщина|Один из шестидесяти гендеров)$',
        profile_get_gender,pass_user_data=True)],
    },
    fallbacks=[],
    )
dp.add_handler(profile)
dp.add_handler(CommandHandler('start', greet_user))#если придет старт, реагируем функцией 
dp.add_handler(RegexHandler('^(Выслушай меня!)$',
                     listen_to_me,))
dp.add_handler(MessageHandler(Filters.text,listen_to_me))
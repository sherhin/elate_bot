import os
import requests
from fake_useragent import FakeUserAgent
import json
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from utils import search_back_keyboard
GOOGLE_API = os.environ.get('GOOGLE_API')
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')


def text_search(user_search):
    url = f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API}&cx={GOOGLE_KEY}&q={user_search}'
    try:
        response = requests.get(url, headers={'User-Agent': FakeUserAgent().chrome})
    except requests.RequestException:
        print('Что-то пошло не так')
    search = json.loads(response.text, encoding='utf-8')
    results = []
    for i in range(6):
        one_result = search['items'][i]
        one_result_title = one_result['title']
        one_result_link = one_result['link']
        try:
            one_result_image = one_result['pagemap']['cse_image'][0]['src']
            result = (one_result_title, one_result_link, one_result_image)
        except KeyError:
            result = (one_result_title, one_result_link)
        results.append(result)
    return results


def search(bot, update, user_data):
    text = 'Что для тебя поискать,солнышко? Напиши, что ты хочешь найти.Если тебе надоест-нажми "Отмену поиска" и "Вернуться".'
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return 'user_search'


def user_search(bot, update, user_data):
    user_data['user_search'] = update.message.text
    search_result = text_search(user_data['user_search'])
    for i in search_result:
        update.message.reply_text("\n\n".join(i), reply_markup=search_back_keyboard())


def stop_search(bot, update, user_data):
    text = 'Поиск завершен'
    update.message.reply_text(text)
    return -1

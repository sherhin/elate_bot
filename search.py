from settings import GOOGLE_API,GOOGLE_KEY
import requests
from fake_useragent import FakeUserAgent
import json

def text_search(user_search):
    url=f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API}&cx={GOOGLE_KEY}&q={user_search}'
    try:
        response=requests.get(url,headers={'User-Agent': FakeUserAgent().chrome})
    except requests.RequestException:
        print('Что-то пошло не так')
    search=json.loads(response.text, encoding='utf-8')
    print (response.headers)
    results=[]
    for i in range (6):
        one_result=search['items'][i]
        one_result_title=one_result['title']
        one_result_link=one_result['link']
        try:
            one_result_image=one_result['pagemap']['cse_image'][0]['src']
            result=(one_result_title,one_result_link,one_result_image)
        except KeyError:
            result=(one_result_title,one_result_link)
        results.append(result)
    return results


def user_search(bot,update):
    user_answer=update.message.text
    search_result=text_search(user_answer)
    for i in search_result:
        update.message.reply_text("\n\n".join(i))
        


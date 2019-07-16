import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
from random import choice
from functools import lru_cache

def get_html(url):
    try:
        result=requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Что-то пошло не так')
        return False

@lru_cache(maxsize=None)
def get_image():
    cat_lst=[]
    url=('http://www.anekdotov-mnogo.ru/content.php?p=smeshnye_koshki&page=')
    for i in range(1,50):
        next_url=url+str((i))
        html=get_html(next_url)
        soup=BeautifulSoup(html,'html.parser')
        image=soup.find_all('div',class_='imagesWidthDiv')
        image=list(image)
        for a in image:
            a=a.find('img')
            image_url=a['src']
            cat_lst.append(image_url)
    return cat_lst
    
def send_cat(bot,update):
    cat_lst=get_image()
    send_cat=choice(cat_lst)
    update.message.reply_text(send_cat)

def send_bash(bot,update):
    url='http://bash.im/random'
    html=get_html(url)
    soup=BeautifulSoup(html,'html.parser')
    quote=soup.find('div', class_="quote__body",text=True)
    pure_quote=quote.text
    update.message.reply_text(str(pure_quote))
       


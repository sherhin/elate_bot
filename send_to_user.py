import requests
from bs4 import BeautifulSoup
from random import choice,random,randrange
from functools import lru_cache
from db import db
from fake_useragent import FakeUserAgent
import json

def get_html(url):
    try:
        result=requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Что-то пошло не так')
        return False

@lru_cache(maxsize=None)
def get_image(bot,job):
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
            cat={'link':image_url}
            db.cats.insert_one(cat)
    return db.cats


def get_mem(bot,job):
    count=1
    while count!=10:
        page_number=str(count)
        page_link = 'http://knowyourmeme.com/memes/all/page/{}'.format(page_number)

        response = requests.get(page_link, headers={'User-Agent': FakeUserAgent().chrome})
        if not response.ok:
            return []
        html = response.content
        soup = BeautifulSoup(html,'html.parser')
        meme_links = soup.findAll('a',class_='photo')
        for elem in meme_links:
            elem=elem.find('img')
            mem_link=elem['data-src']
            mem={'link':mem_link}
            db.memes.insert_one(mem)
        count+=1
    return db.memes



def send_mem(bot,update):
    count = db.memes.count()
    link=db.memes.find()[randrange(count)]
    mem_link=link['link']
    update.message.reply_text(mem_link)
       


def send_cat(bot,update):
    count = db.cats.count()
    link=db.cats.find()[randrange(count)]
    cat_link=link['link']
    update.message.reply_text(cat_link)
    
def send_bash(bot,update):
    url='http://bash.im/random'
    html=get_html(url)
    soup=BeautifulSoup(html,'html.parser')
    quote=soup.find('div', class_="quote__body",text=True)
    pure_quote=quote.text
    update.message.reply_text(str(pure_quote))


def send_joke(bot,update):
    url='http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    res=requests.get(url)
    joke=json.JSONDecoder(strict=False).decode(res.content.decode('windows-1251'))
    update.message.reply_text(joke['content'])

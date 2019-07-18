import requests
from bs4 import BeautifulSoup
from random import choice
from functools import lru_cache
from db import db
from fake_useragent import FakeUserAgent

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


def get_mem():
    mem_list=[]
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
            '''db.memes.insert_one(mem)'''
            mem_list.append(mem_link)
        count+=1
    return mem_list


def send_cat(bot,update):
    cat_lst=get_image()
    send_cat=choice(cat_lst)
    update.message.reply_text(send_cat)


def send_mem(bot,update):
    mem_list=get_mem()
    mem=choice(mem_list)
    update.message.reply_text(mem)
       


'''def send_mem(bot,update):
    send_mem=db.memes.aggregate([{ '$sample': { 'size': 1 } }])
    update.message.reply_text(send_mem)'''

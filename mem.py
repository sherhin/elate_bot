from bs4 import BeautifulSoup
from random import choice
import requests
from fake_useragent import FakeUserAgent
from db import db
import json
import urllib.request

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

def google_search():
    search_text=str()
    page_link='https://www.google.ru/search?newwindow=1&source=hp&ei=F7IsXdvyJpHPrgTIo6joCA&q=kot'
    response=requests.get(page_link,headers={'User-Agent': FakeUserAgent().chrome})
    if not response.ok:
        return []
    else:
        html = response.content
        soup = BeautifulSoup(html,'html.parser')
        meme_links = soup.findAll(class_='iUh30')
    print(meme_links)

def send_joke(bot,update):
    url='http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    res=requests.get(url)
    joke=json.JSONDecoder(strict=False).decode(res.content.decode('windows-1251'))
    update.message.reply_text(joke['content'])
    

def send_mem(bot,update):
    mem_list=get_mem()
    mem=choice(mem_list)
    update.message.reply_text(mem)



'''def send_mem(bot,update):
    send_mem=db.memes.aggregate([{ '$sample': { 'size': 1 } }])
    update.message.reply_text(send_mem)'''

if __name__ == "__main__":
    google_search()
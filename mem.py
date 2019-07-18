from bs4 import BeautifulSoup
import requests
import json


def send_joke(bot,update):
    url='http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    res=requests.get(url)
    joke=json.JSONDecoder(strict=False).decode(res.content.decode('windows-1251'))
    update.message.reply_text(joke['content'])
    


def send_bash(bot,update):
    url='http://bash.im/random'
    html=requests.get(url)
    soup=BeautifulSoup(html,'html.parser')
    quote=soup.find('div', class_="quote__body",text=True)
    pure_quote=quote.text
    update.message.reply_text(str(pure_quote))


import requests
from bs4 import BeautifulSoup
from random import choice

def get_html(url):
    try:
        result=requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Что-то пошло не так')
        return False

def get_image(bot,update):
    cat_lst=[]
    url=get_html('http://www.anekdotov-mnogo.ru/content.php?p=smeshnye_koshki&page=')
    for i in range(1,50):
        next_url=url+str((i))
        soup=BeautifulSoup(next_url,'html.parser')
        image=soup.find_all('div',class_='imagesWidthDiv')
        image=list(image)
        for a in image:
            a=a.find('img')
            image_url=a['src']
            cat_lst.append(image_url)
    send_cat=choice(cat_lst)
    update.message.reply_text(send_cat)
        


import requests
from bs4 import BeautifulSoup
from datetime import datetime
from webapp.model import db, News

URL = 'https://lenta.ru/'

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return None

def get_main_links(html):
    soup = BeautifulSoup(html,'html.parser')
    all_categories = soup.findAll('li', class_="b-sidebar-menu__list-item")
    main_categories =[]
    for link in all_categories:
        categories = link.find('a').text
        url = link.find('a')['href']
        main_categories.append({
            'categories' : categories,
            'url' : 'https://lenta.ru'+url
        })
    return main_categories

def get_news():
    html = get_html(URL)
    links_categories =get_main_links(html)
    for link in links_categories:
        if link['url'] == "https://lenta.ru/":
            continue
    
        html = get_html(link['url'])
        category = link['categories']
        soup = BeautifulSoup(html,'html.parser')
        all_content = soup.findAll('div', class_="item news b-tabloid__topic_news")
        for content in all_content:
            url = content.find('a')['href']
            url = 'https://lenta.ru'+ url
            if check_news_exist(url):
                continue
            title = content.find('a').text
            published= content.find('span', class_='g-date item__date').text[7::]
            html_news = get_html(url)
            soup = BeautifulSoup(html_news,'html.parser')
            #text = soup.find('div', class_="b-text clearfix js-topic__text").text

            if "\xa0" in title:
                title = title.replace("\xa0", " ")
            else:
                continue
            save_news(title,url,published,category)


def check_news_exist(url):
    return bool(News.query.filter(News.url==url).count())


def save_news(title,url,published,category):
        news_news = News(title=title, url=url, published=published, category=category)
        db.session.add(news_news)
        db.session.commit()





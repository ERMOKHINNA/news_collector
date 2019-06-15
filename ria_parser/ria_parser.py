import requests
from bs4 import BeautifulSoup
from flask import current_app


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print ('Some error')
        return False

def get_category():
    html = get_html(current_app.config['URL'])
    if html:
        soup = BeautifulSoup (html, 'html.parser')
        all_news = soup.find('div', class_='footer__rubric-list-item').findAll('a')
        list_of_category = []
        for news in all_news:
            category = news.text
            link = news['href']
            list_of_category.append(
                {
                    'category': category,
                    'link': link
                })
        return list_of_category

def get_news_list():
    list_of_news_links = []
    list_of_category = get_category()

    for link in list_of_category:
        html = get_html(link['link'])
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            all_links_in_category = soup.findAll('div', class_='lenta__item')
            for links in all_links_in_category:
                news_link = links.find('a')['href']
                list_of_news_links.append ({
                    'news_link': news_link,
                    'category': link['category']
                })

    return list_of_news_links

def get_text_of_news():
    news_text = []
    list_of_news = get_news_list()
    for news in list_of_news:
        html = get_html(news['news_link'])
        soup = BeautifulSoup(html, 'html.parser')
        text_of_news = soup.find('div', class_="article__text")
        news_text.append({
            'category': news['category'],
            'text': text_of_news.text
        })
    return news_text


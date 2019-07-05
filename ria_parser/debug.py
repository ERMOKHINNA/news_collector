import requests
from bs4 import BeautifulSoup
from webapp.model import db, News

from datetime import datetime

from webapp import create_app


app = create_app()


class MetaData:
    def __init__(self):
        self.category = None
        self.tags = None
        self.title = None
        self.link = None
        self.image = None


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Some error')
        return None


def get_news_links_from_main(url):
    html = get_html(url)
    all_links = []
    meta_link = MetaData()
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    news_with_link_from_main = soup.findAll('span', class_="share")
    category_with_link = soup.find('div', class_='footer__rubric-list-item').findAll('a')
    for news in news_with_link_from_main + category_with_link:
        if news.get('data-url'):
            meta_link.link = news['data-url']
            all_links.append(meta_link.link)
        elif news.get('href'):
            html = get_html(news['href'])
            if not html:
                return[]
            soup = BeautifulSoup(html, 'html.parser')
            all_links_in_category = soup.findAll('div', class_='lenta__item')
            for links in all_links_in_category:
                meta_link.link = links.find('a')['href']
                all_links.append(meta_link.link)
    return all_links


def meta_info_of_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.findAll('meta')
    meta_list = MetaData()
    for item in all_news:
        meta_list.link = url
        try:
            if item['name'] == 'analytics:rubric':
                meta_list.category = item['content']
            elif item['name'] == 'analytics:tags':
                meta_list.tags = item['content']
            elif item['name'] == 'analytics:title':
                meta_list.title = item['content']

        except KeyError:
            pass
        try:
            if item['property'] == "og:image":
                meta_list.image = item['content']
        except KeyError:
            pass

    return meta_list





def save_news(title, news_link, published, category):
    news_exists = News.query.filter(News.url == news_link).count()

    if not news_exists:
        news_news = News(title=title, url=news_link, published=published, category=category)
        db.session.add(news_news)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        for links in get_news_links_from_main((app.config['RIA_URL'])):
            try:
                part_string = links.split('/')
                date = datetime.strptime(part_string[3], '%Y%m%d')
            except ValueError:
                date = datetime.now()
            news_info = meta_info_of_page(links)

            save_news(news_info.title, news_info.link, date, news_info.category)
            print(news_info.link, news_info.image)






import requests
from bs4 import BeautifulSoup
from webapp.model import db, News

from datetime import datetime

from webapp import create_app


app = create_app()


class MetaData:
    def __init__(self, category, tags, title, link):
        self.category = category
        self.tags = tags
        self.title = title
        self.link = link


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Some error')
        return None


def get_news_link_from_main(url):
    html = get_html(url)
    all_links = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        news_with_link_from_main = soup.findAll('span', class_="share")
        category_with_link = soup.find('div', class_='footer__rubric-list-item').findAll('a')
        for news in (news_with_link_from_main + category_with_link):

            try:
                if news['data-url']:
                    MetaData.link = news['data-url']
                    all_links.append(MetaData.link)
            except KeyError:
                pass
                try:
                    if news['href']:
                        html = get_html(news['href'])
                        if html:
                            soup = BeautifulSoup(html, 'html.parser')
                            all_links_in_category = soup.findAll('div', class_='lenta__item')
                            for links in all_links_in_category:
                                    news_link = links.find('a')['href']
                                    MetaData.link = news_link
                                    all_links.append(MetaData.link)
                except KeyError:
                    pass
        return all_links

##TODO собрать все в кучу
##TODO all_news = soup.findAll('div', class_="cell-extension__item m-with-title")


def meta_info_of_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.findAll('meta')
    meta_list = []
    for item in all_news:
        try:
            if item['name'] == 'analytics:rubric':

                MetaData.category = item['content']
                meta_list.append(MetaData.category)
            elif item['name'] == 'analytics:tags':
                MetaData.tags = item['content']
                meta_list.append(MetaData.tags)
            elif item['name'] == 'analytics:title':
                MetaData.title = item['content']
                meta_list.append(MetaData.title)
        except KeyError:
            pass
    return meta_list


if __name__ == "__main__":
    with app.app_context():
        for obj in meta_info_of_page('https://ria.ru/20190704/1556193923.html'):
            print(MetaData.category,' ', MetaData.tags,' ', MetaData.title )
        print(len(get_news_link_from_main('https://ria.ru')))



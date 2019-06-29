import requests
from bs4 import BeautifulSoup
from ria_parser.model import db, News

from ria_parser.__init__ import create_app


app = create_app()

def get_link(url):
    html = get_html(url)
    all_news = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news1 = soup.findAll('span', class_="share")
        for link in all_news1:
            news_link = link['data-url']
            all_news.append(news_link)
        return all_news


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Some error')
        return None


def meta_info(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.findAll('meta')
    tags_list = {}
    for item in all_news:
        try:
            if item['name'] == 'analytics:rubric':
                category = item['content']
                tags_list['category'] = category
            elif item['name'] == 'analytics:tags':
                tags = item['content']
                tags_list['tags'] = tags
            elif item['name'] == 'analytics:title':
                title = item['content']
                tags_list['title'] = title
        except KeyError:
            pass
    return tags_list

def get_category(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
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

def get_news_list(url):
    list_of_news_links = []
    list_of_category = get_category(url)

    for link in list_of_category:
        html = get_html(link['link'])
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            all_links_in_category = soup.findAll('div', class_='lenta__item')
            for links in all_links_in_category:
                try:
                    news_link = links.find('a')['href']
                    title = links.find('span', class_='lenta__item-text').text

                    category = meta_info(news_link)['category']
                    list_of_news_links.append ({
                        'news_link': news_link,
                        'category': category,

                        'title': title
                    })
                except TypeError:
                    pass

    return list_of_news_links


def get_category_all(url):
    html = get_html(url)
    list_of_category = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.findAll('div', class_="cell-extension__item m-with-title")
        for i in all_news:
            j = i.findAll('a')
            for u in j:

                news = ('https://ria.ru'+ u['href'])
                list_of_category.append(news)

            return list_of_category

def get_else_news_list(url):
    list_of_news_links = []
    list_of_category = get_category_all(url)

    for link in list_of_category:

        html = get_html(link)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            all_links_in_category = soup.findAll('div', class_='lenta__item')
            for links in all_links_in_category:
                news_link = links.find('a')['href']

                try:
                    title = meta_info(news_link)['title']

                    category = meta_info(news_link)['category']
                    list_of_news_links.append({
                        'news_link': news_link,
                        'category': category,

                        'title': title
                    })
                except TypeError:
                    pass

    return list_of_news_links


def get_news_list_from_main(url):
    list_of_news_from_main = []
    list_of_category = get_link(url)

    for link in list_of_category:
        html = get_html(link)
        if html:

            try:
                title = meta_info(link)['title']

                category = meta_info(link)['category']
                list_of_news_from_main.append({
                    'news_link': link,
                    'category': category,

                    'title': title
                    })
            except TypeError:
                pass
    return list_of_news_from_main


##def get_text_of_news(url):
##    news_text = []
##    list_of_news = get_news_list(url)
##    for news in list_of_news:
##        html = get_html(news['news_link'])
##        soup = BeautifulSoup(html, 'html.parser')
##        text_of_news = soup.find('div', class_="article__text")
##        news_text.append({
##            'category': news['category'],
##            'text': text_of_news.text
##        })
##    return news_text

def save_news(title, news_link , category):
    news_exists = News.query.filter(News.url_news == news_link).count()
    if not news_exists:
        news_news = News(title=title, url_news=news_link, category=category)
        db.session.add(news_news)
        db.session.commit()

#TODO добавить теги в базу, добавить словарь слов и тэгов для анализа


#todo вывести дату новости
#todo запуск парсреа по расписанию







if __name__ == "__main__":
    with app.app_context():
        news_list = get_news_list(app.config['URL'])
        news_list_from_main = get_news_list_from_main(app.config['URL'])
        news_list_else = get_else_news_list(app.config['URL'])

        for news in news_list + news_list_from_main + news_list_else:
            save_news(news['title'], news['news_link'], news['category'])
    print("Success save")

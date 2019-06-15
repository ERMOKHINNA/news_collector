import requests
from bs4 import BeautifulSoup
from ria_parser.model import db, News



def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Some error')
        return False

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
                news_link = links.find('a')['href']
                title = links.find('page_title')
                url_news = links.find('page_url')
                list_of_news_links.append ({
                    'news_link': news_link,
                    'category': link['category'],
                    'url_news': url_news
                })

                category = link['category']
 ##               save_news(title, category, url_news)


    return list_of_news_links

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

##def save_news(title, url_news, category):

##    news_news = News(title=title, url_news=url_news, category=category)
##    db.session.add(news_news)
##    db.session.commit()


if __name__ == "__main__":
    get_news_list('https://ria.ru')

import csv
import os
from pprint import pprint
import re
from webapp  import News
from webapp import create_app

with open('/Users/nermohin/projects/diplom_project/news_collector/russian_surnames.csv', 'r', encoding='utf-8') as f:
    fields = ['ID', 'Surname','Sex', 'PeoplesCount','WhenPeoplesCount', 'Source']
    surname_list =[]
    reader = csv.DictReader(f, fields, delimiter=';')
    for surname in reader:
        surname_list.append(surname['Surname'])

surname_set = set(surname_list)
app = create_app()

with app.app_context():
    news_list = News.query
words_in_title = {}
news_with_person = []
for news in news_list:
    set_list = (news.title.split())
    set_news = set(set_list)
    if set_news.intersection(surname_set):
        pattern = set_news.intersection(surname_set)
        if len(str(pattern)) > 7:
            news_with_person.append({

                str(pattern): news.title
             })
            pprint(news_with_person)

print(news_with_person)



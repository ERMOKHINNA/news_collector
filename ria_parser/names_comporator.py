import csv
import os
from pprint import pprint
import re
from ria_parser.model import News
from ria_parser.__init__ import create_app

with open('/Users/nermohin/projects/diplom_project/news_collector/russian_surnames.csv', 'r', encoding='utf-8') as f:
    fields = ['ID', 'Surname','Sex', 'PeoplesCount','WhenPeoplesCount', 'Source']
    surname_list =[]
    reader = csv.DictReader(f, fields, delimiter=';')
    for surname in reader:
        surname_list.append(surname['Surname'])


app = create_app()
##surname_list = ['Путин', 'Медведев', 'Зеленский', 'Нарышкин']
with app.app_context():
    news_list = News.query
words_in_title = {}
news_with_person = []
for title in news_list:

    for surname in surname_list:

        words_in_title['title'] = title.title

        words_in_title['url'] = title.url_news

        pattern = re.search(r'\b' + surname+r'\b', title.title)

        if pattern and len(surname)>3 :
            news_with_person.append({

                pattern.group(): (words_in_title['title'])

            })

            print(pattern.group(), words_in_title['title'])

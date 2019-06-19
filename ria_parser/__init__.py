from flask import Flask, render_template, url_for

from ria_parser.model import db, News




def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)


    @app.route("/")
    def index(page=1):
        page_title = 'Новости'

        news_category = News.query.paginate(page, 10, False).items

        return render_template('index.html', page_title=page_title,  news_category=news_category, page=page)

    return app





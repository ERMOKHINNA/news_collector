from flask import Flask, render_template
from ria_parser.ria_parser import get_text_of_news
from ria_parser.model import db



def create_app():
    app = Flask("__main__")
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        news_category = get_text_of_news()['category']

        return render_template('index.html', page_title=page_title ,  news_category=news_category)

    return app





from flask import Flask, render_template
from ria_parser.ria_parser_news import get_news_list
from ria_parser.model import db
from flask import current_app



def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)
    page_title = 'Новости'

    @app.route("/")
    def index():
        news_category = get_news_list(current_app.config['URL'])
        print (news_category)
        return render_template('index.html', page_title=page_title,  news_category=news_category)

    return app





from flask import Flask, render_template

from webapp.model import db, News

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/<int:page_num>')
    @app.route('/home/<int:page_num>')
    def home(page_num):
        title = 'Новости'
        news_list = News.query.paginate(page=page_num,per_page=10,error_out=True)        

        return render_template('index.html', page_title=title, news_list=news_list)
    return app  




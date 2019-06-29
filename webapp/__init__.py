from flask import Flask, render_template

<<<<<<< HEAD
from webapp.model import db, News
=======
from webapp.model import db,News
>>>>>>> 6393e320386e19720a61cf8320e40c5c642504f7

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)


<<<<<<< HEAD
    # @app.route('/', methods = ['GET', 'POST'])
    # @app.route('/index', methods = ['GET', 'POST'])
    # @app.route('/index/<int:page>', methods = ['GET', 'POST'])
    @app.route('/<int:page_num>')
    @app.route('/home/<int:page_num>')
    def home(page_num):
        title = 'Новости'
        news_list = News.query.paginate(page=page_num,per_page=10,error_out=True)        
=======
    @app.route('/')
    def index():
    	title = "News"
    	news_list = News.query.all()
    	print(news_list)
    	return render_template('index.html', page_title=title,page_news=news_list)
>>>>>>> 6393e320386e19720a61cf8320e40c5c642504f7

        return render_template('index.html', page_title=title, news_list=news_list)
    return app  




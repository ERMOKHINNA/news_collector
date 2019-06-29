import schedule
import time
from webapp import create_app
from webapp.lenta_parser import get_news

def get_save_news():
	print('Parser running......')
	app = create_app()
	with app.app_context():
	    get_news()

schedule.every().day.at("00:00").do(get_save_news)

while True:
    schedule.run_pending()
    time.sleep(1)

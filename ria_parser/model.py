from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class News(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = True)
    url_news = db.Column(db.String, nullable = True)
    category = db.Column(db.String, nullable = True)

    def __repr__(self):
        return '<News {} {} {} {}>'.format(self.id, self.category, self.title, self.url_news)

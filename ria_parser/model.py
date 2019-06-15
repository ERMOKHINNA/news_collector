from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class News(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    text = db.Column(db.Text, nullable = True)
    category = db.Column(db.String, nullable = True)

    def __repr__(self):
        return '<News {} {}>'.format(self.category, self.text)

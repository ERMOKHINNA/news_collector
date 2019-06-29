import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir, '..', 'webapp.db'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
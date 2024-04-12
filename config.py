import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'database.db'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

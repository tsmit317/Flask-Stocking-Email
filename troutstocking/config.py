import os

class Config(object):
    DEBUG = False
    TESTNIG = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///selectedcounties.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE = False

class TestingConfig(Config):
    TESTNIG = True
    SESSION_COOKIE = False
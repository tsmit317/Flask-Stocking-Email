import os
import re

class Config(object):
    DEBUG = False
    TESTNIG = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE = True
    uri = os.environ.get('DATABASE_URL')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI =  uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    TESTNIG = False
    SESSION_COOKIE = True

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE = False

class TestingConfig(Config):
    TESTNIG = True
    SESSION_COOKIE = False
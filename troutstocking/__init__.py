from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

if app.config['ENV'] == 'production':
    print('prod')
    app.config.from_object("troutstocking.config.ProductionConfig")
elif app.config['ENV'] == 'development':
    print('dev')
    app.config.from_object("troutstocking.config.DevelopmentConfig")
elif app.config['ENV'] == 'testing':
    app.config.from_object("troutstocking.config.TestingConfig")

db = SQLAlchemy(app)

from troutstocking import routes

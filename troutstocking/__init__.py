from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object("troutstocking.config.ProductionConfig")
elif app.config['ENV'] == 'development':
    app.config.from_object("troutstocking.config.DevelopmentConfig")
elif app.config['ENV'] == 'testing':
    app.config.from_object("troutstocking.config.TestingConfig")

db = SQLAlchemy(app)

from troutstocking import routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("troutstocking.config.DevelopmentConfig")

db = SQLAlchemy(app)

from troutstocking import routes

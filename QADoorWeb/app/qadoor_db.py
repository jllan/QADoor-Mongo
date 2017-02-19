# from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from .qadoor_app import app

db = MongoEngine(app)
# db = SQLAlchemy(app)
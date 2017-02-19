from .qadoor_app import app
from .qadoor_db import db
from .question import Questions
from .question import question


app.register_blueprint(question)

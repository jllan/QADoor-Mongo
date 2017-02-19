from app import db

class Questions(db.Document):

    _id = db.IntField(primary_key=True)
    url = db.URLField()
    title = db.StringField()
    content = db.StringField()
    is_solved = db.BooleanField(default=0)
    answer_count = db.IntField()
    view_count = db.StringField()
    vote_count = db.StringField()
    tags = db.ListField()
    answers = db.ListField()
    source = db.StringField()
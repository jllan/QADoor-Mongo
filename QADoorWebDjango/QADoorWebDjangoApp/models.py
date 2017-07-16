# from django.db import models
from mongoengine import *
from QADoorWebDjango.settings import DBNAME

connect(DBNAME)

# Create your models here.
class Questions(Document):

    _id = IntField(primary_key=True)
    url = URLField()
    title = StringField()
    content = StringField()
    is_solved = BooleanField(default=0)
    answer_count = IntField()
    view_count = StringField()
    vote_count = StringField()
    tags = ListField()
    answers = ListField()
    source = StringField()

    meta = {'collection': 'questions'}  # 指明连接数据库的哪张表


# for i in Questions.objects[:10]:  # 测试是否连接成功
#     print(i._id)
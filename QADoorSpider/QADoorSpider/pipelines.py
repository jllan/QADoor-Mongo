from pymongo import MongoClient


class QadoorspiderPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client['Questions']
        self.questions = db['questions']

    def process_item(self, item, spider):
        self.questions.find_one_and_update(
            {'_id': item['_id']},
            {'$set': {'title': item['title'], 'content': item['content'], 'answers': item['answers'],
                      'answer_count': item['answer_count'], 'view_count': item['view_count'],
                      'vote_count': item['vote_count'], 'is_solved':item['is_solved'], 'url':item['url'],
                      'tags': item['tags'], 'source': item['source']
                     }
             },
            upsert=True
        )
        return item
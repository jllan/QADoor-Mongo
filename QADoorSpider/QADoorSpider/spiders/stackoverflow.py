import json
import time
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from QADoorSpider.items import QuestionItem

class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        'https://api.stackexchange.com/2.2/questions?key=U4DMV*8nvpm3EOpvf69Rxw((&page=1&pagesize=100&order=desc&sort=votes&site=stackoverflow'
    ]

    def start_requests(self):
        for page in range(100, 200):
            yield Request('https://api.stackexchange.com/2.2/questions?key=U4DMV*8nvpm3EOpvf69Rxw((&page={}&pagesize=100&order=desc&sort=votes&site=stackoverflow'.format(page), callback=self.parse_api)


    """解析api返回的数据"""
    def parse_api(self, response):
        result = json.loads(response.text)
        questions = result['items']
        for q in questions:
            q_item = QuestionItem()
            q_item['_id'] = q['question_id']
            q_item['title'] = q['title']
            q_item['url'] = q['link']
            q_item['tags'] = q['tags']
            q_item['view_count'] = q['view_count']
            q_item['answer_count'] = int(q['answer_count'])
            q_item['vote_count'] = q['score']
            q_item['is_solved'] = 1 if q['is_answered'] else 0
            q_item['content'] = ''
            # q_item['created_date'] = time.strftime('%Y-%m-%d', time.localtime(q['creation_date']))
            # q_item['updated_date'] = time.strftime('%Y-%m-%d', time.localtime(q.get('last_edit_date', q['creation_date'])))
            q_item['source'] = 'so'
            if q_item['answer_count'] >= 1:
                yield Request(url=q_item['url'], meta={'item': q_item}, callback=self.parse_answer)


    """解析每个问题的详细内容及答案"""
    def parse_answer(self, response):
        q_item = response.meta['item']
        selector = Selector(response)
        question_text = selector.xpath('//div[@class="post-text"]').extract()[0]
        answers_text = selector.xpath('//div[@class="post-text"]').extract()[1:]
        answers_votes = selector.xpath('//span[@itemprop="upvoteCount"]/text()').extract()[1:]
        answers = []
        for index, (ans, vote) in enumerate(zip(answers_text, answers_votes)):
            answer = {}
            if q_item['is_solved'] and index == 0:
                answer['is_accepted'] = 1
            else:
                answer['is_accepted'] = 0
            answer['answer_text'] = ans
            answer['answer_votes'] = vote
            answer['answer_id'] = int(str(q_item['_id']) + str(index+1))
            answers.append(answer)
        q_item['content'] = question_text
        q_item['answers'] = answers
        yield q_item

import json
import time
import re
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from QADoorSpider.items import QuestionItem, AnswerItem

class SegmentfaultSpider(scrapy.Spider):
    name = "segmentfault"
    allowed_domains = ["segmentfault.com"]
    start_urls = (
        'https://segmentfault.com/questions?page=1',
    )

    def start_requests(self):
        for page in range(1, 100):
            yield Request('https://segmentfault.com/questions?page={}'.format(page), callback=self.parse_question)


    def parse_question(self, response):
        selector = Selector(response)
        questions = selector.xpath('//section[@class="stream-list__item"]')
        for q in questions:
            q_item = QuestionItem()
            summary = q.xpath('div[@class="summary"]')
            q_item['title'] = summary.xpath('h2/a/text()').extract()[0].strip()
            q_item['url'] = 'https://segmentfault.com' + summary.xpath('h2/a/@href').extract()[0].strip()
            q_item['_id'] = int(q_item['url'].split('/')[-1])
            q_item['tags'] = summary.xpath('ul[contains(@class, "taglist")]/li/a/@data-original-title').extract()
            qa_rank = q.xpath('div[@class="qa-rank"]')
            q_item['vote_count'] = qa_rank.xpath('div[contains(@class, "votes")]/text()').extract()[0].strip()
            q_item['view_count'] = qa_rank.xpath('div[contains(@class, "views")]/span/text()').extract()[0].strip()
            q_item['answer_count'] = int(qa_rank.xpath('div[contains(@class, "answers")]/text()').extract()[0].strip())
            is_solved = qa_rank.xpath('div[contains(@class, "solved")]').extract()
            q_item['is_solved'] = 1 if is_solved else 0
            q_item['source'] = 'sf'
            print(q_item)
            if q_item['answer_count'] >= 1:
                yield Request(url=q_item['url'], meta={'item': q_item}, callback=self.parse_answer)
        '''
        next_page_url = selector.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            print(next_page_url)
            yield Request(next_page_url, callback=self.parse)
        '''

    def parse_answer(self, response):
        q_item = response.meta['item']
        selector = Selector(response)
        question_text = selector.xpath('//div[@class="question fmt"]')[0].extract()
        question_text = re.sub('data-src="/', 'src="https://segmentfault.com/', question_text)
        answers_result = selector.xpath('//article[contains(@class, "clearfix widget-answers__item")]')
        answers = []
        for i, ans in enumerate(answers_result):
            answer = {}
            answer['answer_id'] = int(str(q_item['_id']) + str(i+1))        # question_id=100, answer1_id=1001, answer2_id=1002
            answer['answer_votes'] = ans.xpath('div[@class="post-col"]/div/span/text()')[0].extract()
            answer_text = ans.xpath('div[@class="post-offset"]/div[@class="answer fmt"]')[0].extract()
            answer_text = re.sub('data-src="/', 'src="https://segmentfault.com/', answer_text)
            answer['answer_text'] = answer_text
            if q_item['is_solved'] and i == 0:
                answer['is_accepted'] = 1
            else:
                answer['is_accepted'] = 0
            answers.append(answer)
        q_item['content'] = question_text
        q_item['answers'] = answers

        yield q_item

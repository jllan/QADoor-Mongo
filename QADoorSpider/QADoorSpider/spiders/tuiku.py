import re
from urllib import parse
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from QADoorSpider.items import ArticleItem

class TuikuSpider(scrapy.Spider):
    name = "tuiku"
    # allowed_domains = ["tuicool.com"]
    start_urls = (
        'http://www.tuicool.com/topics/11130000?st=0&lang=1&pn=0',
    )

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=15b13ff61121b1-0679fa0202aad5-1421150f-140000-15b13ff611330d; CNZZDATA5541078=cnzz_eid%3D604530066-1490687638-null%26ntime%3D1500176950; _tuicool_session=BAh7C0kiD3Nlc3Npb25faWQGOgZFRkkiJWZjNTc3MjQxMWU0ZjQ5NmU1N2M4NGViNDc3OTRiODZjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVpEL29teHRTTnhRR1FIeWwycVlOTjIxNzBFUVJpMHhiY1Vnb2swMUh2b009BjsARkkiDHVzZXJfaWQGOwBGaQMWkgJJIg5yZXR1cm5fdG8GOwBGSSIsaHR0cDovL3d3dy50dWljb29sLmNvbS9hcnRpY2xlcy9CYlVKRmI2BjsARkkiDnVzZXJfY2l0eQY7AEZJIgvlhajlm70GOwBUSSITdXNlcl9jaXR5X2NvZGUGOwBGSSIIYWxsBjsAVA%3D%3D--7424f2078d34e840c9197dd1f58c2db057aab636',
        'Host': 'www.tuicool.com',
        'If-None-Match': 'W/"6da29458c549b4788210314b12c8e718"',
        'Referer': 'http://www.tuicool.com/topics',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def start_requests(self):
        for page in range(0, 10):
            if page>1:
                self.headers['Referer'] = 'http://www.tuicool.com/topics/11130000?st=0&lang=1&pn={}'.format(page-1)
            yield Request('http://www.tuicool.com/topics/11130000?st=0&lang=1&pn={}'.format(page), headers=self.headers, callback=self.parse_list)


    def parse_list(self, response):
        selector = Selector(response)
        titles = selector.xpath('//div[@class="title"]/a/@title').extract()
        urls = selector.xpath('//div[@class="title"]/a/@href').extract()
        for title, url in zip(titles, urls):
            q_item = ArticleItem()
            q_item['title'] = title.strip()
            q_item['url'] = parse.urljoin('http://www.tuicool.com/', url)
            # q_item['_id'] = q_item['url'].split('/')[-1]
            yield Request(url=q_item['url'], headers=self.headers, meta={'item': q_item}, callback=self.parse_detail)

    def parse_detail(self, response):
        q_item = response.meta['item']
        selector = Selector(response)
        q_item['pub_date'] = selector.xpath('//span[@class="timestamp"]/text()').extract_first().strip('时间').strip()
        q_item['source'] = selector.xpath('//div[@class="source"]/a[@class="cut cut70"]/text()').extract_first().strip()
        q_item['tags'] = selector.xpath('//span[@class="new-label"]/text()').extract()
        q_item['content'] = selector.xpath('//div[@class="article_body"]').extract_first()
        yield q_item

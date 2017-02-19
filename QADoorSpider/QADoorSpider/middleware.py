# encoding=utf-8
import random
# from cookies import cookies
from .user_agent import agents
from .user_agent import agents_mobile
from .proxy import get_proxy

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        # agent = random.choice(agents_mobile)
        request.headers["User-Agent"] = agent
        # request.headers['Cookie'] = 'prov=244d7b9e-30e6-4f6b-a8db-8ce26444efb6; __qca=P0-1272077840-1457968696850; usr=p=[2|6]; _gat=1; _gat_pageData=1; _ga=GA1.2.1877860909.1480826598'
        # request.headers['Referer'] = 'http://stackoverflow.com/questions'

class ProxyMiddleware(object):
    """ 设置代理 """
    def process_request(self, request, spider):
        proxy = get_proxy()
        print('使用代理：', proxy)
        request.meta['proxy'] = 'http://'+proxy

# class CookiesMiddleware(object):
#     """ 换Cookie """
#
#     def process_request(self, request, spider):
#         cookie = random.choice(cookies)
#         request.cookies = cookie

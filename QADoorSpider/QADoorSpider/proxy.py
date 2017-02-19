import random
import json
import time
import requests
from pymongo import MongoClient
from threading import Thread
from multiprocessing.dummy import Pool

client = MongoClient('localhost', 27017)
db = client['ProxyPool']
proxy_pool = db['proxies']
api = ''


# class ProxyPool(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#
#     def download_proxy(self):
#         if len(self.get_proxy()) < 20:
#             try:
#                 response = requests.get(api)
#             except Exception as e:
#                 print(e)
#             else:
#                 print(response.text)
#                 proxy_list = [proxy.strip() for proxy in response.text.split()]
#                 return proxy_list
#
#     def add_proxy(self, proxy):
#         proxy_pool.find_one_and_update(
#             {'address': proxy},
#             {'error_count': 0},
#             {'status': 1},
#             {'$set': {'proxy': proxy}},
#             upsert=True
#         )
#         return proxy
#
#     def get_proxy(self):
#         proxy_list = []
#         proxies = proxy_pool.find({}, {'_id':0})
#         for proxy in proxies:
#             proxy_list.append(proxy['proxy'])
#         return proxy_list
#
#     def run(self):
#         while True:
#             proxy_new_num = 0
#             proxy_list = self.download_proxy()
#             if proxy_list:
#                 for proxy in proxy_list:
#                     # if self.test_proxy(proxy):
#                     self.add_proxy(proxy)
#                     proxy_new_num += 1
#                 print('新增%s个代理' % proxy_new_num)
#                 print('当前代理池共有%s个代理' % proxy_pool.count())
#             if len(self.get_proxy()) > 20:
#                 time.sleep(100)

class ProxyPool():
    def __init__(self):
        pass

    def download_proxy(self):
        try:
            response = requests.get(api_y2000)
        except Exception as e:
            print(e)
            return None
        else:
            print(response.text)
            proxy_list = [proxy.strip() for proxy in response.text.split()]
            return proxy_list

    def update_proxy(self, address, error_count=0, status=1):
        proxy_pool.find_one_and_update(
            {'address': address},
            {'$set':
                 {'address': address,'error_count': error_count,'status': status}
             },
            upsert=True
        )
        return address

    def del_proxy(self, proxy):
        proxy_pool.find_one_and_delete(
            {'proxy': proxy}
        )

    def test_proxy(self, proxy):
        url = 'https://segmentfault.com'
        try:
            res = requests.get(url, proxies={'https': 'https://' + proxy['address']}, timeout=30)
            print(proxy['address'])
            # if proxy['address'].split(':')[0] != json.loads(res.text)['origin']:
            #     raise Exception('代理透明')
            if res.status_code != 200:
                raise Exception('请求出错')
        except Exception as e:
            print(proxy['address'], e)
            proxy['error_count'] += 1
            if proxy['error_count'] > 8:
                proxy['status'] = 3
            elif proxy['error_count'] > 5:
                proxy['status'] = 2
            # self.del_proxy(proxy)
            # return False
        else:
            proxy['error_count'] = 0 if proxy['error_count'] == 0 else (proxy['error_count']-1)
            # return True
        self.update_proxy(**proxy)
        return proxy

    def get_proxy(self):
        proxy_list = []
        proxies = proxy_pool.find({'status':{"$lt": 2}}, {'_id':0})
        print(proxies)
        for proxy in proxies:
            proxy_list.append(proxy)
        print(proxy_list)
        return proxy_list

    def run(self):
        while True:
            # proxy_list = self.get_proxy()
            if len(self.get_proxy()) < 50:
                proxy_new_num = 0
                proxy_list = self.download_proxy()
                if proxy_list:
                    for address in proxy_list:
                        self.update_proxy(address)
                        proxy_new_num += 1
                    print('新增%s个代理' % proxy_new_num)
            print('当前pool中共有%s个代理' % len(self.get_proxy()))
            pool = Pool(4)
            pool.map(self.test_proxy, self.get_proxy())
            pool.close()
            pool.join()
            # for proxy in proxy_list:
            #     if not self.test_proxy(proxy):
            #         self.del_proxy(proxy)
            print('测试后剩余%s个代理' % len(self.get_proxy()))
            time.sleep(60)

def main():
    proxy_pool = ProxyPool()
    proxy_pool.run()
    print('开始ProxyPool')



def get_proxy():
    proxy_list = [p['address'] for p in proxy_pool.find({'status':{"$lt": 2}}, {'_id': 0})]
    proxy = random.choice(proxy_list)
    print(proxy)
    return proxy


if __name__ == '__main__':
    main()
    # get_proxy()
    # proxy_test = ProxyTest()
    # proxy_test.run()
    # print(proxy)

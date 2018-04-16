import time
import asyncio
from multiprocessing import Process
import asyncio
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError

from .getter import proxy_getter
from .settings import *

class valid_tester(object):
    test_api = TEST_API

    def __init__(self,list):
        self.proxylist = list
        self.valid_list=[]

    async def test_single_proxy(self, proxy):
        #text one proxy, if valid, put them to usable_proxies.
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(self.test_api, proxy=real_proxy, timeout=9) as response:
                        if response.status == 200:
                            self.valid_list.append(proxy)
                            print('Valid proxy', proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Invalid proxy', proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
            print(s)
            pass

    def test_and_update(self,list):
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in list]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('error')
            return None

        f=open('proxy_list','w')
        f.truncate()
        f.writelines(self.valid_list)
        f.close()

class proxy_adder(object):
    def __init__(self,list):
        self.proxylist = list
        self.getter = proxy_getter()
        self.tester = valid_tester(list)

    def add_proxy(self):
        print('start adding')
        add_list=[]
        serch = self.getter
        print(type(serch))
        for proxyurl in serch.crawl_data5u():
            print(proxyurl)
            add_list.append(proxyurl)
        print('stop')

        f=open('proxy_list','a')
        for item in add_list:
            #print('a')
            f.write(item)
            f.write('\n')
        f.close()

class Schedule(object):
    @staticmethod
    def valid_proxy_test(cycle = VALID_PROXY_CHECK):
        print('start test')
        proxy_list=[]

        while True:
            proxy_list=[]
            f = open('proxy_list')
            for line in f:
                proxy_list.append(line)
            f.close()
            count = len(proxy_list)
            if count ==0:
                print('no proxy now,waiting for add')
                time.sleep(cycle)
                continue

            print(proxy_list)

            tester = valid_tester(proxy_list)
            tester.test_and_update(proxy_list)
            time.sleep(cycle)

    @staticmethod
    def check_pool():
        proxy_list = []
        f = open('proxy_list')
        for line in f:
            proxy_list.append(line)
        f.close()

        adder = proxy_adder(proxy_list)

        while True:
            proxy_list=[]
            f = open('proxy_list')
            for line in f:
                proxy_list.append(line)
            f.close()

            count = len(proxy_list)
            if count == 0:
                print('no proxy now,start add')
                adder.add_proxy()
                time.sleep(5)


    def run(self):
        print('process running')
        valid = Process(target=Schedule.valid_proxy_test)
        check = Process(target=Schedule.check_pool)
        valid.start()
        check.start()



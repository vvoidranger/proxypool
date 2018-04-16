import requests
import asyncio
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent,FakeUserAgentError

def get_page(url):
    try:
        ua=UserAgent()
    except FakeUserAgentError:
        pass

    headers={
        'User-Agent':ua.random,
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept':'text/html'
    }
    print('getting',url)
    try:
        r=requests.get(url,headers=headers)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('error')
        return None
from flask import Flask

__all__ =['app']
app = Flask(__name__)

def get_one_proxy():
    f=open('proxy_list','r+')
    a=f.readlines()
    f = open('proxy_list', 'r+')
    f.truncate()
    proxy = a[0]
    del a[0]
    for item in a:
        f.write(item)
    return proxy

@app.route('/')
def index():
    return 'proxypool start'

@app.route('/get')
def get_proxy():
    p = get_one_proxy()
    if p:
        return p
    else:
        return 'no'

if __name__ =='__main__':
    app.run()
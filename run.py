from proxypool.schedule import Schedule
from proxypool.web_api import app

def main():
    s = Schedule()
    s.run()
    #app.run()

if __name__ == '__main__':
    main()
#-*-coding: utf8-*-
import random

import ProxiesDataBase
import spider
import re
import requests
import config
import json

def refresh():
    spider.refresh_db()
    spider.crawl_ip()

def get():
    proxies_dict = {}
    result = ProxiesDataBase.GetItems()
    if result:
        tmp = random.choice(result)
        proxies_dict['http'] = 'http://{}'.format(tmp)
        proxies_dict['https'] = 'https://{}'.format(tmp)
    return proxies_dict


def verify_ip(ip_port):
    ip = ip_port.split(':')[0]
    proxies = {
        "http": "http://{}".format(ip_port), 
        "https": "https://{}".format(ip_port)
    }
    try:
        response = requests.get(config.TestUrl,
                                proxies=proxies,
                                timeout=config.TestTimeOut,
                                headers={
                                    'User-Agent': random.choice(config.UserAgents)
                                })
        print response.text
        origin_ip = json.loads(response.text)['origin']
        delay_time = response.elapsed.microseconds/1000.0 #ms
        print ip, origin_ip, delay_time
        return origin_ip == ip
    except Exception as e:
        print e
        pass
    finally:
        return False

if __name__ == '__main__':
    print verify_ip('61.178.238.122:63000')


#-*-coding: utf8-*-
from random import choice
from re import findall
from requests import get

import config
import ProxiesDataBase
from utils import verify_ip


def get_page_content(tar_url):
    url_content = ""
    try:
        url_content = get(tar_url,
                            headers={
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Encoding': 'gzip, deflate, compress',
                                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ru;q=0.4',
                                'Cache-Control': 'no-cache',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': "1",
                                'User-Agent': choice(config.UserAgents)
        }).text
    except BaseException as e:
        pass
    finally:
        return url_content


def crawl_ip():
    thread_list = []
    ips = []

    for target_url in config.Url_Regular.keys():
        url_content = get_page_content(target_url)
        regular = config.Url_Regular.get(target_url, "")
        tmp_ip_list = findall(regular, url_content)
        for item in tmp_ip_list:
            ips.append("{}:{}".format(item[0], item[1]))

    valid_ips = []
    for ip in ips:
        if verify_ip(ip):
            valid_ips.append(ip)

    return valid_ips




def refresh_db():
    ips = ProxiesDataBase.GetItems()
    valid_ips = []
    for ip in ips:
        if verify_ip(ip):
            valid_ips.append(ip)
    ProxiesDataBase.ClearItems()
    ProxiesDataBase.AddItems(valid_ips)

#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import requests
import random
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
}

def get_proxy_list():
    proxies = []
    # url = "http://ip84.com/dlgn-http"
    url = "http://ip84.com/dl-http"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.findAll("tr")[1:]
    for tr in trs:
        tds = tr.findAll("td")
        if tds[5].text == "0s":
            proxies.append("http://" + tds[0].text + ":" + tds[1].text)
    return proxies

def get_random_proxy():
    proxies = get_proxy_list()
    index = random.randint(0, len(proxies) - 1)
    return {"http" : proxies[index]}


if __name__ == "__main__":
    print(get_random_proxy())
    html = requests.get("http://http://ip84.com/dl-http", headers=headers, timeout = 6, proxies=get_random_proxy()).text
    print(html)

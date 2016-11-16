#!/usr/bin/python
# coding = utf-8
import requests
import json

def __list_service__():
    username = 'CHENJIAXIONG'
    password = '!chen1994'
    url = 'http://inner.kop.com/v2/service'
    res = requests.get(url,auth=(username,password))
    data = json.loads(res.content)
    return data

#if __name__ == "__main__":
#    res = __list_service__()
#    print json.dumps(res,sort_keys=True,indent=2)

#!/usr/bin/python
# coding = utf-8
import requests
import json
import sys
from list_api import __list_api__

def __online_api__(service_name,api_name):
    username = 'CHENJIAXIONG'
    password = '!chen1994'
    flag = 1
    res_api = __list_api__(service_name)
    for api in res_api:
        if api['action'] == api_name:
            id = api['id']
            flag = 2
            url = 'http://inner.kop.com/v2/api/'+str(id)+'/online'
            res = requests.get(url,auth=(username,password))
            return res
    if flag  == 1:
        print 'there is no such api'
#if __name__ == '__main__':
#    result = __online_api__(sys.argv[1],sys.argv[2])
#    print result


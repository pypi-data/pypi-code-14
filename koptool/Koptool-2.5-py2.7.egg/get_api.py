#!/usr/bin/python
# coding = utf-8
import requests
import json
import sys
from list_api import __list_api__

def __get_api__(service_name,api_name):
    username = 'CHENJIAXIONG'
    password = '!chen1994'
    flag = 1
    res_api = __list_api__(service_name)
    for api in res_api:
        if api['action'] == api_name:
            id = api['id']
            flag = 2
            url = 'http://inner.kop.com/v2/api/'+id
            res = requests.get(url,auth=(username,password))
            data = json.loads(res.content)
            return data
    if flag == 1:
        print 'the api_name argv is error!'

#if __name__ == '__main__':           
#    result = __get_api__(sys.argv[1],sys.argv[2])
#    print sys.argv[1]+'  '+sys.argv[2]
 #   print json.dumps(result,indent=2)

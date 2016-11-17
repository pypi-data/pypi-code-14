#!/usr/bin/python
# coding = utf-8
import requests
import json
import sys
from list_service import __list_service__

def __list_api__(name):
    username = 'CHENJIAXIONG'
    password = '!chen1994'
    res_service = __list_service__()
    flag =1
    for service in res_service:
        if service['service_name'] == name:
            flag =2
            id = service['id']
            url = 'http://inner.kop.com/v2/api/service/'+id
            res = requests.get(url,auth=(username,password))
            data = json.loads(res.content)
            return data
    if flag == 1:
        print 'the serice is not exit!'
        
        
#if __name__ == "__main__":
 #   res = __list_api__(sys.argv[1])
#    print sys.argv[1]+' service'
 #   print json.dumps(res,sort_keys=True,indent=2)

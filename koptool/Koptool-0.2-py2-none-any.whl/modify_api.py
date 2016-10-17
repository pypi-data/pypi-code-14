#!/usr/bin/python
# coding = utf-8
import requests
import json
import sys
from offline_api import __offline_api__
from get_api import __get_api__
from online_api import __online_api__


def __update_api__(service_name,api_name,param1,param2):
    username = 'CHENJIAXIONG'
    password = '!chen1994'
    #offline api
    res_offline = __offline_api__(service_name,api_name)
    print 'offline_api '+str(res_offline.status_code)
    if res_offline.status_code == 200 or res_offline.status_code == 400:
        res_api = __get_api__(service_name,api_name)
        str_param2 = param2.split('=')
        if param1 == 'innerapi_desc':
            print str(str_param2[0])+'  '+str_param2[1]
            data_api = res_api['innerapi_desc']
            json_api = json.loads(data_api)
            if str_param2[0] == 'Protocol' or str_param2[0] == 'Timeout':
                if type(json_api[str(str_param2[0])]) == int:
                    json_api[str(str_param2[0])] = int(str_param2[1])
                else :
                    
                    json_api[str(str_param2[0])] = str_param2[1]
            elif str_param2[0] == 'Host' :
                json_api['Host'] = __set_host__(param2)
            
            res_api['innerapi_desc'] = json_api
        else :
            print 'now can not modify openapi_desc!'
      
        #update api
        id = res_api['id']
        
        url = 'http://inner.kop.com/v2/api/'+id
        str_json = json.dumps(res_api[param1])
        
        payload = {param1:str_json}
        res_update = requests.put(url,auth=(username,password),data=payload)
        print '-------------------------------------'
        print 'update api'+str(res_update.status_code)
        if res_update.status_code == 200:
            res_online = __online_api__(service_name,api_name)
            print '-------------------------------------'
            print 'online_api  '+str(res_online.status_code)
           
        else :
            print 'update api fail!'
  

def __set_host__(str):
    res_str = str.split('=')
    res_str_res = res_str[1].split(',')
    x = []
    for res in res_str_res:
        res_json = res.split(':')
        if len(res_json) == 3:
            x.append((res_json[0],res_json[1]+':'+res_json[2]))
        else:
            x.append((res_json[0],res_json[1]))
        
    _ret = dict(x)
    return _ret


#if __name__ == '__main__':
#    print 'modifyapi'
#    __update_api__(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

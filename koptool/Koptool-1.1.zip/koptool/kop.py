#!/usr/lib/python
#coding = utf-8
import argparse
import json
from list_service import __list_service__
from list_api import __list_api__
from get_api import __get_api__
from modify_api import __update_api__
from online_api import __online_api__
from offline_api import __offline_api__
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',  
                                    description='valid subcommands',  
                                    help='additional help',  
                                    dest='subparser_name') 
    
    # A list service command
    list_service_parser = subparsers.add_parser(
        'list_service',help='List All Service')
    
    
    # A list API command
    list_api_parser = subparsers.add_parser(
        'list_api',help='list all api of the right service ')
    list_api_parser.add_argument( 
        'service_name',action='store',
        help='give the right service name')
    

    #A get API command
    get_api_parser = subparsers.add_parser(
        'get_api',help='get the right api')
    get_api_parser.add_argument(
	'service_name',action='store')
    get_api_parser.add_argument(
	'api_name',action='store')
    
    
    #A modify API command
    modify_api_parser = subparsers.add_parser(
        'modify_api',help='modify the right api')
    modify_api_parser.add_argument(
        'service_name',action='store')
    modify_api_parser.add_argument(
        'api_name',action='store')
    modify_api_parser.add_argument(
        'param1',action='store')
    modify_api_parser.add_argument(
        'param2',action='store')
   

    #A online API command
    online_api_parser = subparsers.add_parser(
        'online_api',help='online the right api')
    online_api_parser.add_argument(
        'service_name',action='store')
    online_api_parser.add_argument(
        'api_name',action='store')
   
    
    #A offline API command
    offline_api_parser = subparsers.add_parser(
        'offline_api',help='offline the right api')
    offline_api_parser.add_argument(
        'service_name',action='store')
    offline_api_parser.add_argument(
        'api_name',action='store')
    
    
    results = parser.parse_args()
    
    if results.subparser_name == 'list_service':
        print 'servcie'
        print json.dumps(__list_service__(),sort_keys=True,indent=2)
        
    if results.subparser_name == 'list_api':
        print 'api'
        print json.dumps(__list_api__(results.service_name),sort_keys=True,indent=2)
        
    if results.subparser_name == 'get_api':
        print 'get api'
        print json.dumps(__get_api__(results.service_name,results.api_name),sort_keys=True,indent=2)

    if results.subparser_name == 'modify_api':
        print 'modify_api'
        print json.dumps(__update_api__(results.service_name,results.api_name,results.param1,results.param2),sort_keys=True,indent=2)

    if results.subparser_name == 'online_api':
        print 'online_api'
        print json.dumps(__online_api__(results.service_name,results.api_name),sort_keys=True,indent=2)

    if results.subparser_name == 'offline_api':
        print 'offline_api'
        print json.dumps(__offline_api__(results.service_name,results.api_name),sort_keys=True,indent=2)
    
if __name__ == "__main__":
    main()

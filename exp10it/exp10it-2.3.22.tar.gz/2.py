# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
from exp10it import *
database_init()
import config
crawl_uri("http://www.freebuf.com")
#print get_request("http://blog.creke.net")
#result=collect_uris_from_uri("http://www.freebuf.com")
#print result['y1']

#auto_write_string_to_sql(current_uri,config.db_name,config.all_targets_table_name,"like_admin_login_uris","http_domain",get_http_domain_from_uri(current_uri))
print 66666666666
raw_input()
current_uri="http://blog.creke.net"
result=collect_uris_from_uri(current_uri)
code=result['y2']['code']
title=result['y2']['title']
content=result['y2']['content']
auto_write_string_to_sql(current_uri,config.db_name,config.all_targets_table_name,"uris","http_domain",get_http_domain_from_uri(current_uri))
auto_write_string_to_sql(code,config.db_name,config.all_uris_table_name,"code","uri",current_uri)
auto_write_string_to_sql(title,config.db_name,config.all_uris_table_name,"title","uri",current_uri)
auto_write_string_to_sql(content,config.db_name,config.all_uris_table_name,"content","uri",current_uri)
if like_admin_login_content(content)==True:
    auto_write_string_to_sql(current_uri,config.db_name,config.all_targets_table_name,"like_admin_login_uris","http_domain",get_http_domain_from_uri(current_uri))
    auto_write_string_to_sql(1,config.db_name,config.all_uris_table_name,"like_admin_login_uri","uri",current_uri)
else:
    auto_write_string_to_sql(0,config.db_name,config.all_uris_table_name,"like_admin_login_uri","uri",current_uri)

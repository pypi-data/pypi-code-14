#works in py3,coz mysqlmap module need py3
#works in py2 with selenium not changed best,coz
#the mysqlmap module will use os.system function
#to use the selenium changed version itself
#so here with py3 while selenium changed version or
#selenium not changed version is both ok.
#
#/root/myenv2/bin/python3.5m is the normal python3
#/root/myenv/bin/python3.5 is the changed GoogleScraper script version python
import os
import re
import sys
if sys.version_info>=(3,0,0):
    PY=3
    import importlib,sys
    importlib.reload(sys)
    #sys.setdefaultencoding('utf-8')
else:
    PY=2
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

import mysqlmap
import time
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from exp10it import get_input_intime
from exp10it import checkvpn
from exp10it import execute_sql_in_db
from exp10it import get_scan_finished
from exp10it import set_scan_finished
import config

def main():
    if len(sys.argv)!=2 or sys.argv[1][:4]!="http":
        usage()
        sys.exit(0)
    http_domain=sys.argv[1]

    print('''do you want use 'tor' service in your sqli action? sometimes when your network is not very well,
is not a good idea to use tor,but when your targets has waf,use tor is better.
input Y(y) or N(n) default [N]:>''',end='')
    print('\n')
    choose_tor=get_input_intime('n',5)
    print('\n')
    if choose_tor=='Y' or choose_tor=='y':
        bool_tor=True
    else:
        bool_tor=False

    print('''do you want use 'post' request in your sqli scan? sometimes when you want a faster speed,
use 'get' request is enough,do no need to use 'post' request,meanwhile,when there exists some waf,
use 'get' and 'post' will try too many times's request which will make the waf block you ip,so in these cases,do not use 'post' request,
but use only 'get' request without 'post' request,the number of sqli points will be less in the common sense,
input Y(y) or N(n) default [N]:>''',end='')
    print('\n')
    choose_post=get_input_intime('n',5)
    print('\n')
    if choose_post=='Y' or choose_post=='y':
        post_or_not=True
    else:
        post_or_not=False


    print('''there are two kinds of sqli blew:
1.use "sqlmap_crawl"
2.use "sqlmap-g-nohuman"
input your number here:''',end='')
    print('\n')
    num=str(get_input_intime(1,5))
    print('\n')
    if num==str(1):
        while(1):
            if checkvpn():
                http_domain_sqli_scaned1=get_scan_finished("sqli_scaned",config.db_name,config.targets_table_name,http_domain)
                http_domain_sqli_scaned2=get_scan_finished("sqli_scaned",config.db_name,config.first_targets_table_name,http_domain)
                if http_domain_sqli_scaned1==1 or http_domain_sqli_scaned2==1:
                    break
                elif http_domain_sqli_scaned1==0 or http_domain_sqli_scaned2==0:
                    domain_pang_file="pang/%s_pang.txt" % http_domain.split('/')[-1].replace(".","_")
                    domain_pang_table_name=domain_pang_file[5:-4]
                    if os.path.exists(domain_pang_file):
                        #存在旁站文件说明上次已经进行，但不确定是否所有旁站已经全部扫描完，有可能上次没有扫描完就被中断了
                        with open(domain_pang_file,"r+") as f:
                            domain_pang_list=f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value=re.sub(r"(\s)$","",pang_http_domain)
                                sqli_scaned=get_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)
                                if sqli_scaned==0:
                                    mysqlmap_crawl(pang_http_domain_value,bool_tor,post_or_not)
                                    set_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)
                            result1=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.targets_table_name,http_domain),config.db_name)
                            result2=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.first_targets_table_name,http_domain),config.db_name)
                            if len(result1)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.targets_table_name,http_domain)
                            elif len(result2)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.first_targets_table_name,http_domain)
                            else:
                                print("may be your result from execute_sql_in_db is not what you want from db,check it")
                    else:
                        #不存在旁站文件说明上次没有进行http_domain的旁站获取和sqli扫描
                        os.system("python3 my_bing_domains_v1_alone.py %s" % http_domain.split("/")[-1])
                        with open(domain_pang_file,"r+") as f:
                            domain_pang_list=f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value=re.sub(r"(\s)$","",pang_http_domain)
                                #下面获取如select sqli_scaned from www_freebuf_com_pang where http_domain='http://wit.freebuf.com'的查询结果
                                sqli_scaned=get_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)
                                if sqli_scaned==0:
                                    mysqlmap_crawl(pang_http_domain_value,bool_tor,post_or_not)
                                    set_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)

                            result1=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.targets_table_name,http_domain),config.db_name)
                            result2=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.first_targets_table_name,http_domain),config.db_name)
                            if len(result1)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.targets_table_name,http_domain)
                            elif len(result2)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.first_targets_table_name,http_domain)
                            else:
                                print("may be your result from execute_sql_in_db is not what you want from db,check it")
                    break

                else:
                    print("it seems that one main target's sqli_scaned value you get is not what you want")
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")

    if num==str(2):
        while(1):
            if checkvpn():
                http_domain_sqli_scaned1=get_scan_finished("sqli_scaned",config.db_name,config.targets_table_name,http_domain)
                http_domain_sqli_scaned2=get_scan_finished("sqli_scaned",config.db_name,config.first_targets_table_name,http_domain)
                if http_domain_sqli_scaned1==1 or http_domain_sqli_scaned2==1:
                    break
                elif http_domain_sqli_scaned1==0 or http_domain_sqli_scaned2==0:
                    domain_pang_file="pang/%s_pang.txt" % http_domain.split('/')[-1].replace(".","_")
                    domain_pang_table_name=domain_pang_file[5:-4]
                    if os.path.exists(domain_pang_file):
                        #存在旁站文件说明上次已经进行，但不确定是否所有旁站已经全部扫描完，有可能上次没有扫描完就被中断了
                        with open(domain_pang_file,"r+") as f:
                            domain_pang_list=f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value=re.sub(r"(\s)$","",pang_http_domain)
                                sqli_scaned=get_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)
                                if sqli_scaned==0:
                                    mysqlmap.sqlmap_g_nohuman(pang_http_domain_value,bool_tor,post_or_not)
                                    set_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)
                            result1=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.targets_table_name,http_domain),config.db_name)
                            result2=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.first_targets_table_name,http_domain),config.db_name)
                            if len(result1)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.targets_table_name,http_domain)
                            elif len(result2)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.first_targets_table_name,http_domain)
                            else:
                                print("may be your result from execute_sql_in_db is not what you want from db,check it")


                    else:
                        #不存在旁站文件说明上次没有进行http_domain的旁站获取和sqli扫描
                        os.system("python3 my_bing_domains_v1_alone.py %s" % http_domain.split("/")[-1])
                        with open(domain_pang_file,"r+") as f:
                            domain_pang_list=f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value=re.sub(r"(\s)$","",pang_http_domain)
                                sqli_scaned=get_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)
                                if sqli_scaned==0:
                                    mysqlmap.sqlmap_g_nohuman(pang_http_domain_value,bool_tor,post_or_not)
                                    set_scan_finished("sqli_scaned",config.db_name,domain_pang_table_name,pang_http_domain_value)

                            result1=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.targets_table_name,http_domain),config.db_name)
                            result2=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                                              (config.first_targets_table_name,http_domain),config.db_name)
                            if len(result1)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.targets_table_name,http_domain)
                            elif len(result2)>0:
                                set_scan_finished("sqli_scaned",config.db_name,config.first_targets_table_name,http_domain)
                            else:
                                print("may be your result from execute_sql_in_db is not what you want from db,check it")
                    break

                else:
                    print("it seems that one main target's sqli_scaned value you get is not what you want")
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")


def usage():
    print("-----------------------------------------------------------")
    print("this is a py script to execute sqli scan(include get pang domain sites)\nusage:")
    print("example:python %s https://www.baidu.com" % sys.argv[0])
    print("-----------------------------------------------------------")
if __name__ == "__main__":
    main()

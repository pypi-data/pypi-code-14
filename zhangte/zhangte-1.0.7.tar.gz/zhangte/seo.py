#coding:utf8
try:
    import requests
    from zhangte.base import *
    from .base import *
    from .jiqixuexi import *
    from urllib.parse import quote
    from bs4 import BeautifulSoup
    from Levenshtein import *
    import time
    import urllib
    from pandas import *
    import http.client
    import hashlib
    import urllib
    import random
except Exception as err:
    print (err)





# 获取到调用其的脚本的路径
# PATH = os.path.abspath(os.path.dirname(inspect.stack()[1][1]))
#

class Baidu(Base):
    serp_url_reg = re.compile('<a target="_blank" href=".+?" class="c-showurl".+?">(.+?)</a>|<span class="c-showurl">(.+?)</span>')     #获取搜索结果的url
    rn = 50 #查询排名多少的网站
    pn = 0  #第几页,假如是查询前100名,就写50,前150名,就写100
    VISITS_LOG_PATH = '/data/visits_log/'
    RANK_SCORE = [
        2.856,
        1.923,
        1.020,
        0.814,
        0.750,
        0.572,
        0.401,
        0.441,
        0.553,
        0.670,
    ]

    def __init__(self):
        self.T = False
    #百度实时推送
    def tui(self,domain,token,urls):
        '''百度实时推送,传入域名,token,以及urls(直接read出来的格式)'''
        api = "http://data.zz.baidu.com/urls?site={domain}&token={token}".format(domain=domain,token=token)
        headers = {'User-Agent': 'curl/7.12.1','Content-Type':'text/plain'}
        r = requests.post(api, headers=headers,data = urls)
        print (r.text)

    #配合百度实时推送用的,分割文件长度
    def 分割urls(self,分割文件,分割长度,切片值=0):
        '''
        传入分割文件,以及想要分割的长度就可以了!
        '''
        import math
        urls = open(分割文件).read().split("\n")
        切片值 = 0

        for i in range( math.ceil(len(urls)/分割长度)):
            fl = open("urls_%s.txt" % i,"w")
            str1 = self.ListToStr(urls[切片值:切片值+分割长度],add="\n")
            fl.write(str1)
            fl.close()
            切片值+=分割长度


    #针对编码进行转换
    def bianma(self,kw):
        return quote(kw)


    #百度搜索源代码 - pc
    def baidu_serp(self,kw,skip=False,rn=50):
        ''' 获取SERP搜索源代码'''
        kw = quote(kw)
        while 1:
            url =  'https://www.baidu.com/s?wd=%s&rn=%s' % (kw,rn)
            html = curl(url).text
            if '<img src="http://verify.baidu.com/' in html:
                if skip:
                    return None
                print ('captcha')
                time.sleep(600)
                continue
            else:
                break
        return html


    #百度搜索结果url -pc
    def baidu_serp_urls(self,kw, skip=False,rn=50):
        '''获取搜索结果的urls,如果有百度新闻的页面,可能排名会误差1位,一般都比较准
        T 参数,默认是False,默认不获取真实url,因为这样效率比较低
        当然如果是一些外推网址要查排名的话,肯定是需要获取真实url地址!
        '''
        html = self.baidu_serp(kw,rn=rn)
        soup = BeautifulSoup(html,"lxml")
        urls = []
        #获取真实的url
        if self.T:
            soups = soup.select("h3")
            for soup in soups:
                try:
                    url = soup.select("a")[0].get("href")
                    header = requests.head(url).headers
                    urls.append(header['location'])
                except:
                    urls.append(url)

        else:
            for soup in re.findall(self.serp_url_reg,html):
                for url in soup:
                    if url != "":
                        urls.append(re.sub(re.compile("&nbsp;|</?b>"),'',url))
        return urls

    #获取百度源代码-移动
    def m_baidu_serp(self,kw):
        while 1:
            url = "https://m.baidu.com/s?pn=%s&word=%s" % (self.pn,quote(kw))
            page = urllib.request.urlopen(url)
            html = page.read()
            encoding = "utf-8"
            page.close()
            soup = BeautifulSoup(html,"lxml")
            if not soup.find_all('div', attrs={'class': 'result'}):
                print ('captcha')
                time.sleep(600)
                continue
            break
        return html

    #获取手机百度搜索结果1页
    def m_baidu_serp_urls(self,kw):
        soup = BeautifulSoup(self.m_baidu_serp(kw),"lxml")
        urls = []
        soup = soup.select_one(".results")
        soups = soup.select('div[class^=result]')
        for soup in soups:
            P = re.compile("mu':'(.+?)'")
            try:
                urls.append(re.findall(P,str(soup))[0])
            except:
                continue
        return urls

    #获取手机百度搜索结果 -- 前n页面的所有urls,查询到有排名就结束(节省资源!)
    def n_m_baidu_serp_urls(self,kw,host=None,page=5):
        urls = []
        for i in range(0,page):
            self.pn = i * 10
            urls.extend(self.m_baidu_serp_urls(kw))
            for url in urls:
                if host in url:
                    return urls
        return urls

    #百度收录查询
    def index(self,url):
        """查询百度收录,收录1,未收录0"""
        html = self.baidu_serp(url)
        if '<div class="content_none">' in html:
            return 0
        elif "没有找到该URL" in html:
            return 0

        else:
            return 1

    #百度排名-pc,和手机
    def rank(self,kw, host=None,lp=None,zd="pc",T = False):
        '''
        传入关键词,域名,以及T(完整连接) 获取关键词排名
        '''
        self.T = T
        if not host and not lp:
            return False
        else:

            if zd =="pc":

                urls = self.baidu_serp_urls(kw)
            else:
                #手机端的所有排名
                urls = self.n_m_baidu_serp_urls(kw,host=host)
            if host:
                host = host.replace("http://","")
                for pos, url in enumerate(urls, 1):
                    if host in url:
                        return pos, url
                return -1, '-'
            elif lp:
                for pos, url in enumerate(urls, 1):
                    if '...' not in url:
                        if lp==url:
                            return pos
                    else:
                        start, end = url.split('...')
                        if lp.startswith(start) and lp.endswith(end):
                            return pos
                return -1

    #页面相似度检测
    def Similar(self,url,url2):
        from pyquery import PyQuery as pq
        html1 = pq(url1).text()
        html2 = pq(url2).text()
        print (ratio(html1, html2))

    # 获取根域名
    def root_domain(self,url):
        try:
            url = url.replace('http://', '')
            P = '(\w*\.(com.cn|com|net.cn|net|org.cn|org|gov.cn|gov|cn|mobi|me|info|name|biz|cc|tv|asia|hk|网络|公司|中国)).*$'
            return re.search(P, url).group(1)
        except:
            return '-'

    #获取百度新闻,返回标题和url
    def baidu_news(self,kw,page=0):
        '''获取百度新闻的结果页的链接和对应的url和title,一页50条数据,返回df格式'''
        df = DataFrame(columns=['title','url'])
        url = "http://news.baidu.com/ns?word={}&pn={}&tn=news&rn=50".format(Baidu().bianma(kw),page)
        html = curl(url).content.decode()
        soup = BeautifulSoup(html,"lxml")
        urls = soup.select("h3")
        for h3 in urls:
            data = {}
            data["url"] = h3.select_one("a").get("href")
            data["title"] = h3.text
            df = df.append(Series(data), ignore_index=True)
        return df

    #批量查询收录的代码
    def baiduindexs(self,df,filename):
        '''
        批量查询收录的百度代码,传入df(一般用excel)
        有3个字段,查询日期,url,收录 这3个字段,会直接查询出排名结果!
        filename: 主要是查询后到处的文件,一般建议是一样的!
        '''
        #如果没有http就给他加上http
        df.url = df.url.apply(lambda x:"http://" + x if "http://" not in x else x )

        x = 0
        for i in df.index:
            #如果查询日期 == 今天的话,就不再查询了(一天就查询一次)
            if df["查询日期"][i] == str(Base().today(0)):
                print ("查询过!跳过!")
                pass

            else:
                result = (Baidu().index(df["url"][i]))
                if result == 0:
                    df["收录"][i] = 0
                else:
                    df["收录"][i] = 1
                df["查询日期"][i] = str(Base().today(0))
                print ("%s,%s" % (df["url"][i],df["收录"][i]))
                x +=1
                #查询100条,保存,再读取
                if x % 100 == 0:
                    df.to_excel(filename,index=False)
                    df=read_excel(filename)
                    print (x,"累积100条,导出!")

        df.to_excel(filename,index=False)
        return df


    #分析百度收录的代码啊
    def baiduindex_analyse(self,df1,filename):
        '''
        :param filename: 待分析的文件,在sheet2要定义如下字段:
        meat = {
            "日期":today,
            "总数量":all_data,
            "收录量":index_data,
            "未收录":all_data-index_data,
            "收录率":收录率
        }

        '''
        #收录数量
        index_data = df1[df1.收录 == 1].count()["url"]

        #总数量
        all_data = df1["url"].count()

        #收录率
        收录率 = "%s%%" % round(index_data/all_data* 100,2)
        df2 = read_excel(filename,sheetname=1)
        today = str(Base().today(0))
        #添加一条数据

        meat = {
            "日期":today,
            "总数量":all_data,
            "总收录":index_data,
            "未收录":all_data-index_data,
            "收录率":收录率
        }

        #如果今天不在最后一条数据中就插入,否则就不做操作


        if df2.tail(0)["日期"].count() == 0:
            最后查询日期 = ""
        else:
            最后查询日期 = df2.tail(0)["日期"].values[0]

        if today != 最后查询日期:
            print("今天还未分析,开始写入")
            df2 = df2.append(Series(meat),ignore_index=True)
            writer = ExcelWriter(filename)
            df1.to_excel(writer,'Sheet1')
            df2.to_excel(writer,'Sheet2')
            writer.save()
        else:
            print("分析过了,跳过了,就不写入了!")



class Fanyi(object):
    """
    #设置id和key
    appid = '20160719000025456'
    secretKey = 'UvUw5t4QjaprW3Jaokaz'
    f = Fanyi(appid,secretKey)
    q 翻译的文本
    f.fanyi(q)   #英文翻译
    f.fanyi(q,fromLang="zh",toLang="en")  #中文翻译
    """
    def __init__(self, appid,secretKey):

        super(Fanyi, self).__init__()
        self.appid = appid
        self.secretKey = secretKey

    def fanyi(self,q,fromLang='en',toLang="zh"):

        httpClient = None
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        sign = self.appid+q+str(salt)+self.secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode('utf8'))
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+self.appid+'&q='+urllib.parse.quote(q)+\
                '&from='+fromLang+'&to='+toLang+'&salt='+\
                str(salt)+'&sign='+sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            #response是HTTPResponse对象
            response = httpClient.getresponse()
            a = dict(eval(response.read()))
            list1 = (i["dst"] for i in a["trans_result"])
            return ("\n".join(list1))

        except :
            print ("错误!")
        finally:
            if httpClient:
                httpClient.close()



class SeoBase(Data):

    #传入字符串和标题,自动在文章中插入标题(头中尾)
    def insert_title(self,str1,title='',fenge="。"):
        '''
        使用方式:
        str1:文章,title:需要插入的标题,返回处理后的参数
        '''
        list1 = str1.split("。")
        start = 1
        middle = int(len(list1)/2)
        end = -2
        list1[start] = title + ',' + list1[start]
        list1[middle] = title + ',' + list1[middle]
        list1[end] = title + ',' + list1[end]
        return Base().ListToStr(list1,add="。")

    def GetYuliaokuArticle(self,df,title=''):
        '''
        title: 可以插入标题 (默认3次)
        df,就是目标语料库数据!
        '''
        str1 = self.Creat_content(df)
        return  self.insert_title(str1,title)



#百度实时提交的方法
class 百度批量推送(Baidu):
    # 百度实时提交

    def __init__(self,分割长度,分割文件):
        self.分割长度 = 分割长度
        self.分割文件 = 分割文件

    def get_tui(self):
        return self.tui(self.domain, self.token, self.urls)

    def 批量分割文件(self):
        try:
            # 首先对文件进行分割一下!
            self.分割urls(self.分割文件, 分割长度=self.分割长度)

            # 分割完了以后,把文件删除
            os.system("rm %s" % self.分割文件)
        except Exception as e:
            print (e)
            print("没有分割文件,跳过")

    # 主要运行函数
    def main(self):
        '''
        返回的是还有多少urls的文件,可用根据还剩余多少,做判断,如果等于0就不提交了!
        '''
        self.批量分割文件()
        # 随机提取一个文件出来,进行提交
        list1 = [file for file in os.listdir(os.getcwd()) if "txt" in file]
        if len(list1) != 0:
            filename = random.choice(list1)
            self.urls = open(filename).read()

            # 开始提交文件的urls ,这个注释去掉
            self.get_tui()

            # 删除这个文件  测试成功的话,这个注释也去掉!
            os.system("rm %s" % filename)
            print("提交成功,%s成功删除!" % filename)
            return len(list1)


if __name__ == '__main__':
    url = "http://blog.sina.com.cn/s/blog_12b8c51100102wo28.html"
    print (Baidu().index(url))
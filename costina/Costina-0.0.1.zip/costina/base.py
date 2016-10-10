#coding:utf-8
'''
@Author: Xiaozhe Yaoi <i@askfermi.me>
'''
import gevent
from bs4 import BeautifulSoup
from basemodel import *
import requests
class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance  



'''
Base Spider defines the crawling site using requests.
'''
class BaseSpider(Singleton):
    def __init__(self,url):
        self.url=url
    def crawl(self):
        '''
        rewrite this method to support get & post method.
        '''
        r=requests.get(self.url)
        return r.text

class BaseExtractor():
    def __init__(self):
        pass
    def setContent(self,content):
        self.soup=BeautifulSoup(content)
    def select(self,stat):
        return self.soup.select(stat)
    '''
    Override this method to implements different extract
    '''
    def extract(self):
        pass

'''
Helper Functions
'''
def store(obj):
    gevent.sleep(random.randint(0,2)*0.001)
    print 'store called'
    if isinstance(obj,Model):
        obj.save()
        print 'store called'
    else:
        raise ValueError('Object Type Error')
        print 'type error'

def crawl(url,extractor):
    crawler = BaseSpider(url)
    text=crawler.crawl()
    extractor.setContent(text)
    extractor.extract()

class CrawlerFactory():
    def __init__(self,num_of_threads):
        self.num_of_threads=num_of_threads+1
    def start(self,urls,extractor):
        threads=[gevent.spawn(crawl,url,extractor) for url in urls]
        print threads
        gevent.joinall(threads)
    def start_sync(self,urls,extractor):
        for each in urls:
            crawl(each,extractor)
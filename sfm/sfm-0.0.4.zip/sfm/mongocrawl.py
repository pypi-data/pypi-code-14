#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A MongoDB backed data crawler framework.

为了说明方便, 我们以http://www.cvs.com/网站为例, 任务是爬所有CVS Store的信息。

- Task: 是待爬的资源的抽象概念。每一个

"""

import pickle
import pymongo
import mongoengine                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
from bs4 import BeautifulSoup
from sfm.fingerprint import fingerprint
from sfm.mongoengine_mate import ExtendedDocument
from requests_spider import spider

#--- Framework Code ---
class Task(object):
    """
    
    **中文文档**
    
    
    对单条Task进行抓取的过程如下:
    
    1. 取出Task文档。
    2. 根据文档中的信息, 定位到数据资源所在, 通常是是一个Url。
    3. (可选) 将下载下来的数据储存在 _crawled 项中。注意MongoDB有16MB的文档大小
      限制,所以最好下载下来后先用gzip压缩。
    4. (可选) 直接将爬下来的东西放到你所想要的地方。
    5. 如果爬虫顺利完成任务, 则将 _finished 标记为True。
    
    待爬的对象。需要有一个 ``_id`` 项作为全局唯一标识符
    
    - _id: Collection唯一的标识符
    - _finished: boolean, 是否已完成
    - _status: int, 爬虫的状态
    - _crawled: downloaded, 已下载下来的数据, 通常经过了压缩
    """
    _id = mongoengine.StringField(primary_key=True)
    _finished = mongoengine.BooleanField(default=False)
    _status = mongoengine.IntField()
    _crawled = mongoengine.BinaryField()
    
    __meta__ = {
        "store": True, # 是否自动将爬下来的数据保存。
        "compress": True, # 是否压缩爬下来的数据。若store为False, 则该项无效。
        "status": dict(), # 爬虫状态码的定义, 是一个 {int: str} 的字典
    }
    
    def task_plan(self, *args, **kwargs):
        """
        """
        raise NotImplementedError

    @classmethod
    def get_to_crawl(cls, *args, **kwargs):
        """
        """
        try:
            return cls.objects(_finished=False)
        except:
            raise NotImplementedError
    
    @classmethod
    def get_data(cls, *args, **kwargs):
        """
        :param input: 文档本身
        :returns: 已下载的数据
        """
        raise NotImplementedError
    
    @classmethod
    def parse_data(cls):
        pass
    
    
    
    
#--- Real Code ---
mongoengine.connect("cvs")

class StateIndex(ExtendedDocument, mongoengine.Document, Task):
    _id = mongoengine.StringField(primary_key=True)
    _finished = mongoengine.BooleanField(default=False)
    
    def get_url(self):
        return self._id
    
    @staticmethod
    def get_state(html):
        soup = BeautifulSoup(html)
        for div in soup.find_all("div", class_="states"):
            for a in div.find_all("a"):
                state = State(_id=a["href"].split("/")[-1], name=a.text.strip())
                yield state
                
    @staticmethod
    def task_plan():
        state_index = StateIndex(
            _id="http://www.cvs.com/store-locator/cvs-pharmacy-locations",
        )
        state_index.save()
        
    @staticmethod
    def crawl_all(iterable):
        for state_index in iterable:
            url = state_index.get_url()
            html = spider.get_html(url, encoding="utf-8")
            if html:
                for state in StateIndex.get_state(html):
                    state.save()
                    state_index._crawled = pickle.dumps(html)
                    state_index._finished = True
                    state_index.save()
        

class State(ExtendedDocument, mongoengine.Document, Task):
    name = mongoengine.StringField()
    
    def get_url(self):
        url = "http://www.cvs.com/store-locator/cvs-pharmacy-locations/%s" % self._id
        return url
    
    @staticmethod
    def get_city(html):
        soup = BeautifulSoup(html)
        for div in soup.find_all("div", class_="states"):
            for a in div.find_all("a"):
                city = City(_id=a["href"].split("/")[-1])
                yield city
        
    @staticmethod
    def crawl_all(iterable):
        for state in iterable:
            url = state.get_url()
            html = spider.get_html(url, encoding="utf-8")
            if html:
                for state in StateIndex.get_state(html):
                    state.save()
                    state_index._crawled = pickle.dumps(html)
                    state_index._finished = True
                    state_index.save()
                    
class City(ExtendedDocument, mongoengine.Document, Task):
    pass


# StateIndex.task_plan()
StateIndex.crawl_all(StateIndex.get_to_crawl())    
# coding:utf8
try:
    import requests
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
    import json
    import numpy as np
    import math
except Exception as err:
    print(err)


# 生意参谋相关的方法类集合
class Sycm(Base):
    核心数据 = mongo("淘宝", "店铺核心指标")
    流失分析概要 = mongo("淘宝", "流失数据概要")
    def __init__(self):
        try:
            cookies = open("../../cookie.txt").read()
            self.cookies = self.get_cookies(cookies)
        except:
            print ("cookies没有成功获取,可能会影响使用!")
    # 导入到mongodb里面(cookies的数据要正确)
    def intomongodb(self, day):
        cookies = open("../../cookie.txt").read()
        cookies = self.get_cookies(cookies)
        date = "{date}%7C{date}".format(date=day)

        if not self.核心数据.find({"date": {'$in': [day]}}, {}).count():
            # 先把全部的数据导入的mongodb中
            url_1 = "https://sycm.taobao.com/bda/summary/getShopSummaryTrend.json?dateType=day&indexCode=%s&dateRange="
            list1 = ["payRate", "uv", "dsrScore", "pv", "payAmt", "successRefundAmt", "payPct"]

            for types in list1:
                url = url_1 % types + date
                data = self.get_json(url, cookies)
                data["date"] = day
                data["types"] = "_" + types
                self.核心数据.insert_one(data)
        else:
            print("今日查询过,不再插入了!")

    # 获取数据
    def get_json(self, url, cookies):
        r = requests.get(url, cookies=self.cookies)
        return json.loads(r.content.decode())["content"]["data"]

    # 获取指定日期的数据 - 核心数据
    def get_data(self, sheet, day, col):
        '''
        传入数据连接,指定日期,以及指定的列,获取对应的数据
        '''
        return sheet.find_one(
            {"date": {"$in": [day]}, "types": {"$in": [col]}},
            {"_id": 0}
        )

    # 获取生成参谋流失概要的数据
    def 流失概要(self, day):
        list1 = "paylosAmt%2CpaylosByrCnt%2CpaylossRate%2CpaylosCltByrCnt%2CpaylosCartByrCnt"
        list2 = "paylosCltUnByrCnt%2CpaylosCartUnByrCnt%2CpaylosUnUv%2CpaylosItmCnt%2CpaylosShopCnt"
        url_1 = "https://sycm.taobao.com/ci/item/paylos.json?dateRange={day}%7C{day}&dateType=day&page={page}&contentType=simple&pageSize=10&order=desc&orderBy=paylosAmt&indexCode="

        # 需要封装起来!
        if not self.流失分析概要.find({"date": {'$in': [day]}}, {}).count():
            for page in range(1, 10):
                url = url_1.format(day=day, page=page) + list1 + "%2C" + list2
                r = curl(url, cookies=self.cookies)
                # 获取数据
                datas = json.loads(r.content.decode())["data"]["data"]
                # 如果没有数据,就停止了!(超过页数了!)
                if not datas:
                    break
                print(len(datas))
                for data in datas:
                    data["date"] = day
                    # 如果没查询 就查询
                    self.流失分析概要.insert_one(data)

    # 流失概要取值的小函数
    def get_value(self, x):
        return x["value"]

    # 可用复用的代码,计算动态评分数
    def get_dsr(self, now, hope, appraiser):
        return (hope * appraiser - now * appraiser) / (5 - hope)

    # 获取评价人数(动态评分的)
    def get_pingjia(self):
        url = "https://rate.taobao.com/user-rate-UvCNSOmx4vFNWvWTT.htm?spm=a1z10.1-b.d4918101.3.BaYdiE"
        html = curl(url,cookies=self.cookies)
        soup = BeautifulSoup(html.content.decode("gbk"), "lxml")
        tags = soup.select("div.total > span:nth-of-type(2)")
        return max([int(tag.text) for tag in tags])

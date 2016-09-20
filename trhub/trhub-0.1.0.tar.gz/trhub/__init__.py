# -*- coding: UTF-8 -*-
"""
TrHub
=====
"""
import redis
import time
import pandas as pd
import format as fm
import trhub.utils as utils
import trhub.utils.mkdown as mkdown


@utils.singleton
class TuRingDataHub:
    def __init__(self, host="localhost", port=6379, db=0, password=""):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None
        self.isinit = False
        self.init(host, port, db, password)

    def init(self, host="localhost", port=6379, db=0, password=""):
        """
            初始化redis
        """
        if self.isinit:
            return self.client
        else:
            self.client = redis.StrictRedis(host, port, db, password)
            self.isinit = True
        return self.client

    def getdays(self, market="SSE", code="000001", type="INDEX", begintime=(time.time() - (60 * 60 * 24 * 500)) * 1000,
                endtime=time.time() * 1000, num=None):
        """
            通过 市场,代码,类型 得到日K数据,默认500天前
            Key:
                SS.DAYS.${CODE}.DATE.${MARKET}.${TYPE}
        """
        key = ".".join(("SS", "DAYS", code, "DATE", market, type))
        if num is not None:
            result = self.client.zrange(key, -num, -1)
        else:
            result = self.client.zrangebyscore(key, begintime, endtime)
        return pd.DataFrame(map(lambda x: pd.Series(fm.kline(x.split(","))), result))

    def gettradecode(self, market="SSE", type="A_STOCK", day=None):
        """
            通过 市场,类型,日期 得到交易日的 交易品种, 不提供日期,默认 最新交易日
            Key:
                SS.MARKET.CODE.${DATE}.${MARKET}.${TYPE}
        """

        if day is None:
            day = self.getlasttradeday(market=market, type=type)["date"][0]

        key = ".".join(("SS", "MARKET", "CODE", day, market, type))
        result = self.client.zrange(key, 0, -1, withscores=True)

        def tuple2array(i, i2):
            item = i.split(",")
            item.append(i2)
            return item

        return pd.DataFrame(map(lambda x: pd.Series(fm.code(tuple2array(x[0], x[1]))), result))

    def gettradedays(self, market="SSE", type="A_STOCK", begin=0, end=-1):
        """
            通过 市场,类型 得到 交易日
            Key:
                SS.TRADETIME.DAYS.DATE.${MARKET}.${TYPE}
        """
        key = ".".join(("SS", "TRADETIME", "DAYS", "DATE", market, type))
        result = self.client.zrange(key, begin, end, withscores=True)
        return pd.DataFrame(map(lambda x: pd.Series(fm.tradeday([x[0], x[1]])), result))

    def getlasttradeday(self, market="SSE", type="A_STOCK"):
        """
            通过 市场,类型 得到 最后交易日
            Key:
                SS.TRADETIME.DAYS.DATE.${MARKET}.${TYPE}
        """
        return self.gettradedays(market=market, type=type, begin=-1, end=-1)

    def saveresult(self, list, direction="UP", name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        """
            把结果保存到数据库中
            Key:
                SE.QUANT.${NAME}.${DATE}.${MARKET}.${TYPE}
        """
        name = name.upper()
        market = market.upper()
        type = type.upper()
        key = ".".join(("SE", "QUANT", name + "(" + direction + ")", date, market, type))
        self.client.sadd(key, *list)

    def saveupresult(self, list, name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        """
            存储涨的股票代码列表
        """
        self.saveresult(list, "UP", name, market, type, date)

    def savedownresult(self, list, name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        """
            存储跌的股票代码列表
        """
        self.saveresult(list, "DOWN", name, market, type, date)

    def getresult(self, direction="UP", name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        """
            得到存储在redis中的结果
            Key:
                SE.QUANT.${NAME}.${DATE}.${MARKET}.${TYPE}
        """
        name = name.upper()
        market = market.upper()
        type = type.upper()
        key = ".".join(("SE", "QUANT", name + "(" + direction + ")", date, market, type))
        return self.client.smembers(key)

    def getupresult(self, name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        return self.getresult("UP", name, market, type, date)

    def getdownresult(self, name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        return self.getresult("DOWN", name, market, type, date)

    def getresulthtml(self, name="DEMO", market="SZSE", type="A_STOCK", date="20160918"):
        md = mkdown.directionresult()
        upresult = self.getupresult(name, market, type, date)
        for item in upresult:
            md + [market, item, type, "UP"]
        downresult = self.getdownresult(name, market, type, date)
        for item in downresult:
            md + [market, item, type, "DOWN"]
        return md.tohtml()


DHub = TuRingDataHub

# -*- coding: UTF-8 -*-
"""
TrHub
=====
"""
import redis
import time
import pandas as pd;
import format as fm;
import utils


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
                endtime=time.time() * 1000):
        """
            通过 市场,代码,类型 得到日K数据,默认100天前
            Key:
                SS.DAYS.${CODE}.DATE.${MARKET}.${TYPE}
        """
        key = ".".join(("SS", "DAYS", code, "DATE", market, type))
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


DHub = TuRingDataHub

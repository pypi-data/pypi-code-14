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
        :param market: 市场
        :param code: 代码
        :param type: 股票类型
        :param begintime: 开始时间戳
        :param endtime: 结束时间戳
        :param num: 想获得数据条数
        :return: DataFrame数据
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
        :param market: 市场
        :param type: 股票类型
        :param day: 交易日 例如：20160926
        :return: DataFrame类型股票列表
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
        :param market: 市场
        :param type: 股票类型
        :param begin: 开始点
        :param end: 结束点
        :return: DataFrame交易日
        """
        key = ".".join(("SS", "TRADETIME", "DAYS", "DATE", market, type))
        result = self.client.zrange(key, begin, end, withscores=True)
        return pd.DataFrame(map(lambda x: pd.Series(fm.tradeday([x[0], x[1]])), result))

    def getlasttradeday(self, market="SSE", type="A_STOCK"):
        """
         通过 市场,类型 得到 最后交易日
            Key:
                SS.TRADETIME.DAYS.DATE.${MARKET}.${TYPE}
        :param market: 市场
        :param type: 股票类型
        :return: 最新交易日
        """
        return self.gettradedays(market=market, type=type, begin=-1, end=-1)

    def saveresult(self, list, direction, name, market, type, date="20160918"):
        """
         把结果保存到数据库中
            Key:
                SE.QUANT.${NAME}.${DATE}.${MARKET}.${TYPE}
        :param list: 股票列表 example:  [000001, 000002, ...]
        :param direction: 方向 看涨看跌
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param date: 日期 example: 20160918
        """
        if len(list) == 0:
            return
        name = name.upper()
        market = market.upper()
        type = type.upper()
        key = ".".join(("SE", "QUANT", name + "(" + direction + ")", date, market, type))
        self.client.sadd(key, *list)

    def saveupresult(self, list, name, market, type, date):
        """
        存储涨的股票代码列表
        :param list: 股票列表 example:  [000001, 000002, ...]
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param date: 日期 example: 20160918
        """
        self.saveresult(list, "UP", name, market, type, date)

    def savedownresult(self, list, name, market, type, date):
        """
        存储跌的股票代码列表
        :param list: 股票列表 example:  [000001, 000002, ...]
        :param name: 策略名
        :param market: 市场
        :param type: 市场类型
        :param date: 日期 example: 20160918
        """
        self.saveresult(list, "DOWN", name, market, type, date)

    def saveinspectresult(self, up, down, upright, downright, name, type, date):
        """
        存储验证结果
        :param up: 看涨股票数
        :param down:看跌股票数
        :param upright:看涨预测对的数目
        :param downright:看跌预测对的数目
        :param name: 策略名
        :param type:股票类型
        :param date:日期
        """
        name = name.upper()
        type = type.upper()
        date = date.upper()
        key = '.'.join(('SE', 'INSPECT', name, date, type))
        data = {'uplength': up, 'downlength': down, 'upright': upright, 'downright': downright}
        self.client.sadd(key, data)

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

    def inspect(self, name, type, date=None):
        """
        检查预测正确性 并存入redis
        :param name: 策略名
        :param date: 日期  example:20160926
        :param type: 股票类型
        """
        # if date is not None:
        date = self.gettradedays(begin=-2, end=-2)['date'][0]
        lastTime = self.getlasttradeday()['date'][0]
        szseup = self.inspectresult(name=name, market='SZSE', type=type, date=date, dic='up')
        # print '-------------------'
        szsedown = self.inspectresult(name=name, market='SZSE', type=type, date=date, dic='down')
        # print '-------------------'
        sseup = self.inspectresult(name=name, market='SSE', type=type, date=date, dic='up')
        # print '-------------------'
        ssedown = self.inspectresult(name=name, market='SSE', type=type, date=date, dic='down')
        self.saveinspectresult(name=name, type='A_STOCK', date=lastTime, up=szseup['length'] + sseup['length'], down=szsedown['length'] + ssedown['length'], upright=szseup['right'] + sseup['right'], downright=szsedown['right'] + ssedown['right'])

    def inspectresult(self, name, market, type, date, dic='up'):
        dic = dic.upper()
        right = 0
        if dic == 'UP':
            result = self.getupresult(name=name, market=market, type=type, date=date)
        else:
            result = self.getdownresult(name=name, market=market, type=type, date=date)
        length = len(result)
        for code in result:
            temp = self.getdays(market=market, code=code, type=type, num=2)
            Todayclose = temp.at[len(temp) - 1, 'close']
            refclose = temp.at[len(temp) - 2, 'close']
            ud = Todayclose - refclose
            if dic == 'UP' and ud > 0:
                right += 1
            if dic == 'DOWN' and ud < 0:
                right += 1
        return {'right': right, 'length': length}

    def getinspectresult(self, name='DEMO', type='A_STOCK', date='20160918'):
        """
        得到存储在redis中的结果
        key: SE.QUANT.${NAME}.${DATE}.${TYPE}
        :param name:策略名
        :param type:股票类型
        :param date:日期
        :return: 结果集合
        """
        name = name.upper()
        type = type.upper()
        key = '.'.join(('SE', 'INSPECT', name, date, type))
        return self.client.smembers(key)
DHub = TuRingDataHub

# -*- coding: UTF-8 -*-
import pandas as pd
import trhub.format as fm


class Market:
    def __init__(self, context):
        self.context = context
        self.context.market = self

    def get_trade_code(self, market="SSE", type="A_STOCK", day=None):
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
            day = self.get_last_tradeday(market=market, type=type)["date"][0]

        key = ".".join(("SS", "MARKET", "CODE", day, market, type))
        result = self.context.client.zrange(key, 0, -1, withscores=True)

        def tuple2array(i, i2):
            item = i.split(",")
            item.append(i2)
            return item

        return pd.DataFrame(map(lambda x: pd.Series(fm.code(tuple2array(x[0], x[1]))), result))

    def get_trade_days(self, market="SSE", type="A_STOCK", begin=0, end=-1):
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
        result = self.context.client.zrange(key, begin, end, withscores=True)
        return pd.DataFrame(map(lambda x: pd.Series(fm.tradeday([x[0], x[1]])), result))

    def get_last_tradeday(self, market="SSE", type="A_STOCK"):
        """
         通过 市场,类型 得到 最后交易日
            Key:
                SS.TRADETIME.DAYS.DATE.${MARKET}.${TYPE}
        :param market: 市场
        :param type: 股票类型
        :return: 最新交易日
        """
        return self.get_trade_days(market=market, type=type, begin=-1, end=-1)

    def get_last_trade_day(self, market="SSE", type="A_STOCK"):
        """
         通过 市场,类型 得到 最后交易日
            Key:
                SS.TRADETIME.DAYS.DATE.${MARKET}.${TYPE}
        :param market: 市场
        :param type: 股票类型
        :return: 最新交易日
        """
        return self.get_trade_days(market=market, type=type, begin=-1, end=-1)

    def get_pre_trade_day(self, market, type):
        """
        通过 市场,类型 得到 上一个交易日
            Key:
                SS.TRADETIME.DAYS.DATE.${MARKET}.${TYPE}
        :param market: 市场
        :param type: 股票类型
        :return: 最新交易日
        """
        return self.get_trade_days(market=market, type=type, begin=-2, end=-2)

    def get_trade_days(self, market="SSE", type="A_STOCK", begin=0, end=-1):
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
        result = self.context.client.zrange(key, begin, end, withscores=True)
        return pd.DataFrame(map(lambda x: pd.Series(fm.tradeday([x[0], x[1]])), result))

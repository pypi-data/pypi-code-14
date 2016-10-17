# -*- coding: UTF-8 -*-
import time
import pandas as pd
import trhub.format as fm


class History:
    def __init__(self, context):
        self.context = context;
        self.context.history = self

    def get_days(self, market="SSE", type="INDEX", code="000001", data_type="",
                 begin_time=(time.time() - (60 * 60 * 24 * 500)) * 1000, end_time=time.time() * 1000, num=None):
        """
        获得日K 数据
        :param market: 市场
        :param type: 股票类型
        :param code: 代码
        :param data_type: 数据类型 example： （QFQ）
        :param begin_time: 开始时间戳
        :param end_time: 结束时间戳
        :param num: 需要数据条数
        :return: DataFrame 类型 数据
        """
        key = ".".join(("SS", "DAYS" + data_type, code, "DATE", market, type))
        # print key, begin_time, end_time, num
        if num is not None:
            result = self.context.client.zrange(key, -num, -1)
        else:
            result = self.context.client.zrangebyscore(key, begin_time, end_time);
        return pd.DataFrame(map(lambda x: pd.Series(fm.kline(x.split(","))), result))

    def get_minutes(self, market="SSE", type="INDEX", code="000001", date=None):
        if date is None:
            date = self.context.market.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("HS", "MINUTE", code, date, market, type))
        result = self.context.client.hgetall(key)
        return pd.DataFrame(map(lambda x: pd.Series(fm.minute(x, result[x].split(","))), result))

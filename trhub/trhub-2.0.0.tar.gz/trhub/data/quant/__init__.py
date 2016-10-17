# -*- coding: UTF-8 -*-
class Quant:
    def __init__(self, context):
        self.context = context
        self.context.quant = self

    def set_quant_result(self, name, market, type, maps, date=None):
        """
        存储 策略 结果
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param maps: 数据 example: [key:value, key:value .....]
        :param date: 日期
        """
        if date is None:
            date = self.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("SS", "QUANT", name, date, market, type))
        self.context.client.zadd(key, **maps)

    def get_quant_result(self, name, market, type, date=None):
        """
        获得策略结果
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param date: 日期
        :return: example:[(000001,21),(000002,-9),(000008,5),....]
        """
        if date is None:
            date = self.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("SS", "QUANT", name, date, market, type))
        return self.context.client.zrange(key, 0, -1, withscores=True)
        # return self.get_quant_result_by_score(name, market, type, date, -100000000, +100000000)

    def get_quant_result_by_score(self, name, market, type, begin_score, end_score, date=None):
        """
        通过 score 获得策略结果
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param begin_score: 起始分
        :param end_score: 结束分
        :param date: 日期
        :return: [000001, 000002,.....]
        """
        if date is None:
            date = self.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("SS", "QUANT", name, date, market, type))
        return self.context.client.zrangebyscore(key, begin_score, end_score)

    def set_quant_accuracy(self, name, market, type, score, date=None):
        """
        存储 策略 验证 结果
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param score: 分数
        :param date: 日期
        """
        if score == 0:
            return
        if date is None:
            date = self.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("HS", "ACCURACY", name, "DATE", market, type))
        self.context.client.hset(key, date, score)
        ss_key = ".".join(("SS", "ACCURACY", "QUANT", date, market, type))
        self.context.client.zadd(ss_key, score, name)

    def get_quant_accuracy(self, name, market, type):
        """
        获得历史准确率
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :return: (key:value)
        """
        key = ".".join(("HS", "ACCURACY", name, "DATE", market, type))
        return self.context.client.hgetall(key)

    def set_item_result(self, name, direction, market, type, code, score, date=None):
        """
        存储 详细验证 结果
        :param name: 策略名
        :param direction: RIGHT or WRONG
        :param market: 市场
        :param type: 股票类型
        :param code: 股票代码
        :param score: 看涨跌分数
        :param date: 日期
        """
        if date is None:
            date = self.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("HS", direction, name, date, market, type))
        self.context.client.hset(key, code, score)

    def get_item_result(self, name, direction, market, type, date=None):
        """
        获取 详细验证 结果
        :param name: 策略名
        :param direction: RIGHT or WRONG
        :param market: 市场
        :param type: 股票类型
        :param date: 日期
        """
        if date is None:
            date = self.get_last_trade_day(market, type)["date"][0]
        key = ".".join(("HS", direction, name, date, market, type))
        return self.context.client.hgetall(key)

    def ver_quant(self, name, market, type, date=None):
        """
        验证 准确度
        :param name: 策略名
        :param market: 市场
        :param type: 股票类型
        :param date: 日期
        :return: 准确率
        """
        if date is None:
            date = self.get_pre_trade_day(market, type)["date"][0]
        result = self.get_quant_result(name, market, type, date)
        ok = 0.0
        no = 0.0
        for i in range(len(result)):
            item = result[i]
            days = self.get_days(market=market, type=type, code=item[0], num=2)
            tmp_tag = None
            # print time.localtime(days["time"][0] / 1000), time.localtime(days["time"][1] / 1000)
            if item[1] * (days["close"][1] - days["close"][0]) > 0:
                ok += 1
                tmp_tag = "RIGHT"
            elif item[1] != 0:
                no += 1
                tmp_tag = "WRONG"
            if tmp_tag is not None:
                self.set_item_result(name, tmp_tag, market, type, item[0], item[1], date)
        if ok == 0 and no == 0:
            return 0
        accuracy = ok / (ok + no)
        self.set_quant_accuracy(name, market, type, accuracy, date)
        return accuracy


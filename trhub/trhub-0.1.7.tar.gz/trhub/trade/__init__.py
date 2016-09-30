# -*- coding: UTF-8 -*-
# import trhub.utils as utils
# @utils.singleton

class Trade:
    def __init__(self, name, money):
        self.name = name
        self.records = []
        self.money = money
        self.trades = {"up": [], "down": []}

    def opentrade(self, direction="up", time=None, money=None):
        if self.money >= money:
            self.trades[direction].append({"time": time, "money": money})
            self.money -= money
            # else:
            #     print "没有足够的钱咯~"

    def closetrade(self, direction="up", time=None, money=None):
        if len(self.trades[direction]) != 0:
            trade = self.trades[direction].pop()
            self.records.append(
                {"direction": direction, "open": trade["money"], "close": money, "opentime": trade["time"],
                 "closetime": time})
            if direction is "up":
                self.money += money
            else:
                self.money += (trade["money"] * 2 - money)

    def open(self, direction="up", hand=1, money=None, time=None):
        if money is not None:
            for i in range(0, hand):
                self.opentrade(direction, time, money)

    def close(self, direction="up", hand=1, money=None, time=None):
        if money is not None:
            for i in range(0, hand):
                self.closetrade(direction, time, money)

    def buy(self, hand=1, money=None, time=None):
        self.open("up", hand, money, time)

    def sell(self, hand=1, money=None, time=None):
        self.open("down", hand, money, time)

    def closebuy(self, hand=1, money=None, time=None):
        self.close("up", hand, money, time)

    def closesell(self, hand=1, money=None, time=None):
        self.close("down", hand, money, time)

    def myvalue(self, money=None):
        mymoney = self.money + len(self.trades["up"]) * money;
        for i in range(0, len(self.trades["down"])):
            item = self.trades["down"][i]
            # 看空算法 现今价值  = 成本+(成本-现价)
            # 根据算数优化, 现今价值 = 成本*2 - 现价
            mymoney += (item["money"] * 2 - money)
            # return len(self.trades["up"]) * money + len(self.trades["down"]) * money + self.money
        return mymoney
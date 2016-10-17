class Trade:
    def __init__(self, context):
        self.context = context
        self.context.trade = self

    def get_money(self, name, tick):
        key = ".".join(("SS", "TRADE", "ACCOUNT", "DATE", tick.market, tick.type))
        return self.context.client.zscore(key, name)

    def set_money(self, name, tick, money):
        key = ".".join(("SS", "TRADE", "ACCOUNT", "DATE", tick.market, tick.type))
        return self.context.client.zadd(key, name, money)

    def inc_money(self, name, tick, money):
        key = ".".join(("SS", "TRADE", "ACCOUNT", "DATE", tick.market, tick.type))
        return self.context.client.zincrby(key, name, money)

    def add_trade(self, name, tick, hand):
        key = ".".join(("SS", "TRADE_RECORD", name, "DATE", tick.market, type))
        return self.context.client.zadd(key, tick.close * hand, ",".join(tick.code, tick.price, hand))

    def open(self, name, market, type, code, price, hand):
        total = price * hand
        money = self.get_money(name, market, type)
        if total > money:
            return False
        else:
            self.inc_money(name, market, type, total)
            self.add_trade(name, market, type, code, price, hand)
            return True

    # def close(self, name, market, type, code, price, hand):

# -*- coding: UTF-8 -*-
"""
TrHub
=====
"""
import redis
import format as fm
import trhub.utils as utils

from trhub.data.market import Market
from trhub.data.history import History
from trhub.data.quant import Quant


@utils.singleton
class TuRingDataHub:
    def __init__(self, host="localhost", port=6379, db=0, password=""):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None
        self.is_init = False
        self.init(host, port, db, password)
        self.market = Market(self)
        self.history = History(self)
        self.quant = Quant(self)

    def init(self, host="localhost", port=6379, db=0, password=""):
        """
            初始化redis
        """
        if self.is_init:
            return self.client
        else:
            self.client = redis.StrictRedis(host, port, db, password)
            self.is_init = True
        return self.client


DHub = TuRingDataHub

# coding=utf8

import base64
import os
import sys
import time
from collections import namedtuple
from hashlib import sha1
from hmac import new as hmac

import pandas as pd


class ConstConf:
    MAX_CODE_LEN = 64
    CODE_LEN = 6
    ENCODING = "utf-8"
    DEBUG_BASE_URL = "http://192.168.100.34:17081"
    BASE_URL = "http://api.ichinascope.com"


class Conf(ConstConf):
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".token.cfg")
    max_display_rows = 5
    max_display_columns = 50
    debug = False
    version = None

    def __init__(self):
        self.__token = None
        self.__access_key = None
        self.__t = None

    def set_option(self, pat, value):
        """请参考pandas.set_option方法
        """
        pd.set_option(pat, value)

    @property
    def token(self):
        """获取token
        Returns
        -------
            str
        """
        if not self.__token:
            if not os.path.exists(self.cache_path):
                raise Exception("token未设置")

            pkl = pd.read_pickle(self.cache_path)
            if not (pkl.__contains__("access_key") and pkl.__contains__("secret_key")):
                raise Exception("token获取失败或未设置")

            self.__t = str(time.time())
            self.__access_key = pkl["access_key"]

            if sys.version > "3":
                self.__token = base64.encodebytes(hmac(
                    bytearray("%s,%s,%s" % (pkl["access_key"], self.__t, pkl["secret_key"]), "utf-8"),
                    digestmod=sha1).digest())[:-1]
            else:
                self.__token = base64.encodestring(hmac(
                    "%s,%s,%s" % (pkl["access_key"], self.__t, pkl["secret_key"]),
                    digestmod=sha1).digest())[:-1]

        Token = namedtuple("Token", ["access_key", "time", "token"])
        return Token(access_key=self.__access_key,
                     time=self.__t,
                     token=self.__token)

    def set_token(self, access_key, secret_key):
        """设置token

        Parameters
        ----------
        access_key:str
        secret_key:str
        Returns
        -------

        """
        ser = pd.Series({"access_key": access_key, "secret_key": secret_key})
        ser.to_pickle(self.cache_path)
        self.__token = None


config = Conf()
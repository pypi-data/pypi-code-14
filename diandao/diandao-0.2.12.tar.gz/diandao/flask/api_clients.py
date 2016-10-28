# -*- coding: utf-8 -*-
import requests
from hashlib import md5
from diandao import JSON
from diandao.flask import app


class ClientMeta(type):
    """ Client Meta Class
    """

    def __getattr__(cls, method):
        return getattr(cls(), method, None)

    def __str__(cls):
        return 'Interface Client <%s>' % (cls.__name__,)


class BaseClient(object):
    """ Remote Interface Base Client
        创建远程接口客户端, 用于请求远程接口
    """
    __metaclass__ = ClientMeta
    # 远程接口名, 默认为Client的类名去掉"Client"
    __interface__ = None
    # 远程接口API, 可在configs中配置, 配置名为 "CLIENT_%s_API" % self.__interface__
    # 如 http://127.0.0.1:9001/rpc
    __api__ = None

    def __init__(self, interface=None, api=None):
        if interface is None:
            interface = self.__default_interface()
        if api is None:
            api = self.__default_api()
        self.__interface__ = interface
        self.__api__ = api

    def __default_interface(self):
        cn = self.__class__.__name__
        return cn[0:-6]

    def __default_api(self):
        return self.__api__

    def api(self):
        cfname = "CLIENT_%s_API" % self.__interface__.upper()
        return app.config.get(cfname, self.__api__)

    def execute(self, method, *args, **kwargs):
        """ 接口执行方法
        """
        pass

    def __getattr__(self, method):
        def callmethod(*args, **kwargs):
            return self.execute(method, *args, **kwargs)

        return callmethod

    pass


class PHPV1Client(BaseClient):
    """ php老接口, 对应if.diandao.org

    """

    version = "0.0.1"

    def __init__(self, *args, **kwargs):
        BaseClient.__init__(self, *args, **kwargs)
        if not self.__api__:
            self.__api__ = "http://if.diandao.org/%s/index.php" % (self.__interface__.lower())

    def execute(self, method, *args, **kwargs):
        """ 接口执行方法
        """
        if not self.__api__:
            raise Exception("Undefined API for %s" % self.__class__.__name__)
        # 参数数据
        params = dict(
            mod=self.__interface__,
            act=method,
            platform="diandao"
        )
        params.update(**kwargs)
        randkey = []
        pkeys = params.keys()
        pkeys.sort()
        key = pkeys[-1]
        randkey.append("%s%s" % (key, params[key]))
        # 添加干扰
        randkey = "".join(randkey) + "The key for Programming"
        # md5
        randkey = md5(randkey).hexdigest()
        # 前9位字符
        randkey = randkey[0:9]
        # http请求参数
        data = dict(
            randkey=randkey,
            c_version=self.version,
            parameter=JSON.stringify(params)
        )
        res = requests.get(self.api(), data)

        if not res.ok:
            raise Exception(res.reason, res.status_code)

        result = res.json()
        if result['code'] > 0:
            raise Exception("[Error] code:%s; desc:%s" % (result.code, result.desc))
        return result['data']

    pass

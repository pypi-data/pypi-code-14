# -*- coding: utf-8 -*-
import logging
import requests
from uuid import uuid1

import json
from redis import StrictRedis
from django.conf import settings

logger = logging.getLogger("djdg_common_verify")

def connect():
    redis_conf = settings.REDIS
    check_keys = ["HOST", "PORT", "DB", "PASSWORD"]
    if not all(map(lambda x: x in redis_conf, check_keys)):
        raise {"data": "required\n".join([i for i in check_keys if i not in redis_conf])}
    return StrictRedis(host=redis_conf["HOST"], port=redis_conf["PORT"], db=redis_conf["DB"],
                       password=redis_conf["PASSWORD"])


class ActionKeyOperation(object):
    def __init__(self, key_type, app_type, action_type, expire, user_id, data=None, log=None):
        """
        :param key_type: key类型
        :param action_type: 操作类型
        :param app_type: app 类型
        :param expire: 过期时间 秒为单位
        :param user_id: user id
        :param data: data, 当data不为空则将key设置为data，类型为json
        :param log: log对象，配置log记录
        """
        self.connect = connect()
        self.key_type = key_type if key_type else 'session'
        self.app_type = app_type
        self.action_type = action_type if action_type else 'token'
        self.expire = expire
        self.user_id = user_id
        self.key = self.get_key()
        self.data = data
        self.log = log
        if self.log:
            log.info(
                """
    [key_type]: {key_type}
    [app_type]: {app_type}
    [action_type]: {action_type}
    [expire]: {expire} seconds
    [user_id]: {user_id}
    [key]: {key}
    [data]: {data}
    [token]: {token}
                """.format(key_type=self.key_type,
                           app_type=self.app_type,
                           action_type=self.action_type,
                           expire=self.expire,
                           user_id=self.user_id,
                           key=self.key,
                           data=self.data,
                           token=self.token)
            )

    def tokenexsits(self):
        token = self.connect.exists(self.key)
        if not token:
            return False
        else:
            return True

    def settoken(self):
        # 重新设置过期时间
        if self.data:
            token = json.dumps(self.data)
        else:
            if self.tokenexsits():
                token = self.connect.get(self.key)
            else:
                while True:
                    token = '{key_type}:{uuid}'.format(key_type=self.key_type, uuid=uuid1())
                    if not self.connect.exists(token):
                        break
        self.connect.setex(token, self.expire, self.user_id)
        self.connect.setex(self.key, self.expire, token)
        if self.log:
            self.log.info("""
    resettoken:
    [key]: {key}
    [expire]: {expire} seconds
    [token]: {token}
            """.format(key=self.key, expire=self.expire, token=self.token))
            return True

    def get_key(self):
        key = "user:{user_id}:{app_type}:{action_type}".format(user_id=self.user_id,
                                                               app_type=self.app_type,
                                                               action_type=self.action_type)
        return key

    def get_token_rest_expiretime(self):
        return self.connect.ttl(self.token)

    def get_key_rest_expiretime(self):
        return self.connect.ttl(self.key)

    @property
    def is_validkey(self):
        t = self.get_key_rest_expiretime()
        return True if int(t) >= -1 else False

    @property
    def is_validtoken(self):
        t = self.get_token_rest_expiretime()
        return True if int(t) >= -1 else False

    @property
    def token(self):
        return self.connect.get(self.key)

# -*- coding: utf-8 -*-


class Blocker(object):

    rds = None

    def __init__(self, rds):
        self.rds = rds

    def is_blocked(self, key):
        return self.rds.get(key)

    def block(self, key, timeout):
        """
        只有key不存在的时候，才重新设置，否则会导致block timeout一直延长
        :param key:
        :param timeout: 超时时间，<0 代表无限
        :return:
        """
        if timeout >= 0:
            return self.rds.set(key, 1, ex=timeout, nx=True)
        else:
            return self.rds.set(key, 1, nx=True)

    def unblock(self, key):
        return self.rds.delete(key)

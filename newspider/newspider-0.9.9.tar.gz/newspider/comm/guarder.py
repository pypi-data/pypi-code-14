# -*- coding: utf-8 -*-

import time
from urlparse import urlparse

from newspider.comm.utils import Utils


class Guarder:

    def __init__(self,config):
        self.config = config
        self.map_last_req = {}

    def check(self,url):
        interval = self.config.get('GUARD_INTERVAL',0)
        if interval == 0: return True # 0表示禁用门卫功能,所以直接返回即可

        host = urlparse(url).hostname
        current_time = int(time.time())
        last_time = self.map_last_req.get(Utils.md5(host),0)
        if current_time - last_time > interval:
            self.map_last_req[Utils.md5(host)] = current_time #记录这次的时间
            return True
        else:
            return False
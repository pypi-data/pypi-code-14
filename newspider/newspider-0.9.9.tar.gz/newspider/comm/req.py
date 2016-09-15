# -*- coding: utf-8 -*-
import requests
import logging

class Req:

    def __init__(self,config):
        self.config = config
        self.session = requests.session()
        self.logger = logging.getLogger('Newspider')


    def get(self,url):
        user_agent = self.config.get('USER_AGENT','newspider/1.0')
        headers = {'user-agent': user_agent}

        #检测代理
        http_proxy = self.config.get('HTTP_PROXY',None)
        proxies = {}
        if http_proxy is not None:
            proxies['http'] = http_proxy

        self.logger.debug("Requesting content for url: %s" % url)
        r = self.session.get(url, headers=headers,proxies = proxies)
        self.logger.debug("Response code: %d" % r.status_code)
        if r.content is not None:
            return r.content
        else:
            return None



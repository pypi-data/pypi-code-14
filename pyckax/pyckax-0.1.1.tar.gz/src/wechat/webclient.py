'''
'''
import time, re, os
from ..storage import Scraper

class WebClient(Scraper):
    # +-------------------------------------------------------------------------
    def __init__(self):
        pass
    # +-------------------------------------------------------------------------
    def run(self):
        print('Start Web WeChat Client')
        able, uuid = self.__getUUID()
        if not able:
            return False
        print(uuid)
        self.__genQRCode(uuid)
    # +-------------------------------------------------------------------------
    def __getUUID(self):
        '''
        第一步，获取UUID
        '''
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid': 'wx782c26e4c19acffb',
            'fun': 'new',
            'lang': 'zh_CN',
            '_': int(time.time())
        }
        data = self.post(url,params)
        expression = 'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+)"'
        match = re.search(expression, data)
        if match:
            code = match.group(1)
            if code == '200':
                return (True,match.group(2))
            else:
                return (False,code)
        return (False,'unknown')
    # +-------------------------------------------------------------------------
    def __genQRCode(self,uuid):
        '''
        第二步，生成二维码
        '''
        url = 'https://login.weixin.qq.com/qrcode/'+uuid
        params = {
            't': 'webwx',
            '_': int(time.time())
        }
        data = self.post(url,params)
        if data == '': return
        #path = self.__saveFile()
    # +-------------------------------------------------------------------------
    def __login(self,tip,uuid):
        '''
        第三步，等待用户登录
        '''
        url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip='
        url += tip + '&uuid=' + uuid + '&_=' + int(time.time())
        data = self.get(url)
    # +-------------------------------------------------------------------------
    def __webwxnewloginpage(self):
        '''
        第四步，登录获取Cookie
        '''
        url = 'https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxloginpage'
    # +-------------------------------------------------------------------------
    def __saveFile(self, filename, data):
        pass

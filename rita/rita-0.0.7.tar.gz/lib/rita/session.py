# -*- coding: utf-8 -*-
try:
    from http.cookies import SimpleCookie
except:
    from Cookie import SimpleCookie
#
from uuid import uuid4

class ISessionStore:
    def exists(self, sessionid):
        pass
    
    def get(self, sessionid, key):
        pass

    def set(self, sessionid, key, value, create=False):
        pass
    
    def delete(self, sessionid, key=None):
        pass

    def open(self):
        pass

    def close(self):
        pass
    
    def getByUserId(self, userid):
        pass

class HttpSession(object):
    def __init__(self, appbase, expires=-1, cookie_name="__psessionid", httponly=True, secure=False):
        #同じクエリを何度も発行しないようにするためのキャッシュ
        self._cachedValues = {}
        self._sessiondb = appbase.get_http_session_store()

        self._type = 'cookie'
        self._appbase = appbase
        self.env = self._appbase.env
        self.expires = expires
        self.cookie_name = cookie_name
        self.httponly = httponly
        self.secure = secure
        if not "HTTP_COOKIE" in self.env:
            self._type = 'url'

        #これはNoneになる可能性がある
        self.sessionid = self._getSessionId()
        
    @staticmethod
    def invalidateBySessionId(sessionid):
        db = HttpSession._getSessionStore()
        db.delete(sessionid)
        db.close()

    def close(self):
        self._sessiondb.close()

    def begin(self, name, value):
        self.invalidate()
        self.sessionid = str(uuid4())
        self._createPair(name, value)
        self["_rita_hidden_token"] = str(uuid4())

    def exists(self):
        self._sessiondb.exists(self.sessionid)

    def getByUserId(self, userid):
        return self._sessiondb.getByUserId(userid)

    def _createPair(self, name, value):
        #今の値があればそれを返す
        current = self[name]
        if current != None:return current
        self._sessiondb.set(self.sessionid, name, value, True) 

    def set_to_header(self, **kargs):
        sessionid = self.sessionid
        #Cookieヘッダーに書き出す値を取得
        dic = {'path':'/'}
        if self.expires != -1:
            dic['expires'] = self.expires

        for key, value in kargs.items():
            dic[key] = value
        cookie = SimpleCookie()

        #memo:セッションIDはDBにあるものか、サーバー側で生成したものしか使ってはならない
        if self.sessionid == None:
            raise "empty sessionid"
        cookie[self.cookie_name] = self.sessionid
        for k in dic.keys():
            cookie[self.cookie_name][k] = dic[k]
        cookie[self.cookie_name]["httponly"] = self.httponly
        cookie[self.cookie_name]["secure"] = self.secure
        self._appbase.header("Set-Cookie", cookie[self.cookie_name].OutputString())

    def _getSessionId(self):
        if self._type == 'cookie':
            cookie = SimpleCookie(self.env["HTTP_COOKIE"])
            if self.cookie_name in cookie:
                return cookie[self.cookie_name].value
        elif self._type == 'url':
            if not self.cookie_name in self._appbase._params:
                return None
            return self._appbase._params[self.cookie_name].value
        else:
            return None

    def __getitem__(self, name):
        return self._sessiondb.get(self.sessionid, name)

    def __setitem__(self, name, value):
        self._sessiondb.set(self.sessionid, name, value)

    def __delitem__(self, name):
        self._sessiondb.delete(self.sessionid, name)

    def invalidate(self):
        cookie = SimpleCookie()

        #expireを-1で出力（=Cookieの削除）
        cookie[self.cookie_name] = self.sessionid
        cookie[self.cookie_name]["path"] = "/"
        cookie[self.cookie_name]["expires"] = "-1"
        self._appbase.header("Set-Cookie", cookie[self.cookie_name].OutputString())
        
        try:
            self._sessiondb.delete(self.sessionid)
        except:
            self.sessionid = None
            return
        self.sessionid = None

    def get_url(self, url):
        if self._type == 'cookie':
            return url

        if url.find('?') > -1:
            url += "&"
        else:
            url += "?"
        url += self.cookie_name + "=" + self.sessionid
        return url

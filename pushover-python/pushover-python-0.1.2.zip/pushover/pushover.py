# coding=utf-8
"""
    pushover api
    ~~~~~~~~~~~~
     `https://pushover.net/api'
"""

import sys
import time
import json
import logging

is_py2 = (sys.version_info[0] == 2)
if is_py2:
    from httplib import HTTPSConnection
    from urllib import urlencode
    str_type = unicode
else:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode
    str_type = str


logger = logging.getLogger(__name__)
try:
    logger.addHandler(logging.NullHandler())
except AttributeError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass
    logger.addHandler(NullHandler())


class PushoverException(Exception):
    pass


class Pushover(object):
    """"""

    def __init__(self, token, user):
        self._token = token
        self._user = user

    def notify(self, message, title="", **kwargs):
        """
        priority (-2 -1 0 1 2)
        sound (bike,bugle,cashregister,classical,cosmic,falling,gamelan,
               incoming,intermission,magic,mechanical,pianobar,siren,spacealarm,
               tugboat,alien,climb,persistent,echo,updown,none)
        """
        try:
            data = {
                'token': self._token,
                'user': self._user,
                'title': title,
                'message': message,
            }
            data.update(kwargs)
            payload = []
            for (k, v) in data.items():
                if isinstance(v, str_type):
                    payload.append((k, v.encode("utf-8")))
                else:
                    payload.append((k, v))
            logging.info(json.dumps(payload))
            headers = {"Content-type": "application/x-www-form-urlencoded",}
            conn = HTTPSConnection("api.pushover.net")
            params = urlencode(payload)
            conn.request("POST", "/1/messages.json", params, headers)
            rsp = conn.getresponse()
            if rsp.status != 200:
                raise PushoverException("pushover:{0}".format(rsp.status))
            conn.close()
        except Exception as e:
            raise PushoverException("exception:{0!r}".format(e))


if __name__ == '__main__':
    logger.addHandler(logging.StreamHandler())
    logger.setLevel("DEBUG")
    p = Pushover("h1gzv64NTSq3Ua9eNyEaxUplvIv8Nz",
                 "GnAflo6NBk7RvHQaPCOP3IbMMcopEN")
    p.notify('<a href="https://www.baidu.com">点我！</a>', "标题", html=1)

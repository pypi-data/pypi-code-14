import hmac
import hashlib
import re
from urllib.parse import urlparse
from datetime import datetime

class Authorizer():
    def __init__(self, api_key, secret, scope, service):
        self.api_key = api_key # per team key, available on LiveStories platform
        self.secret = secret #
        self.scope = scope # permissions given to request
        self.service = service # service used by request

    def _signing_key(self, date):
        h = hmac.new(bytearray(self.secret, 'utf-8'), digestmod=hashlib.sha256)
        h.update(bytearray(date, 'utf-8'))

        h = hmac.new(bytearray(h.hexdigest(), 'utf-8'), digestmod=hashlib.sha256)
        h.update(bytearray(self.scope, 'utf-8'))

        h = hmac.new(bytearray(h.hexdigest(), 'utf-8'), digestmod=hashlib.sha256)
        h.update(bytearray(self.service, 'utf-8'))

        return h.hexdigest()

    def _header_text(self, headers):
        if headers is None:
            return ''

        return "\n".join([k.lower() + ":" + re.sub("\s+", " ", headers[k].strip())
                                                        for k in headers ])
    def _header_list(self, headers):
        if headers is None:
            return ''

        return ";".join([k.lower() for k in headers])

    def _credential_text(self, date):
        return "{0}/{1}/{2}/{3}".format(self.api_key, date, self.scope, self.service)

    def authorization_string(self, method, url, sign_headers=None, expire=None):
        if expire:
            expire = expire.strftime("%Y%m%dT%H%M%S%z")
        else:
            expire = ''

        req_url = urlparse(url)

        request_date = datetime.utcnow()
        date_short = request_date.strftime("%Y%m%d")
        date_long =  request_date.strftime("%Y%m%dT%H%M%S%z")

        cred = self._credential_text(date_short)
        head = self._header_text(sign_headers)
        head_list = self._header_list(sign_headers)

        query = "date={0}&credential={1}&headers={2}&expire={3}".format(date_long, cred, head_list, expire)

        if len( req_url.query ) > 0:
            query = req_url.query + '&' + query

        request_text = "{0}\n{1}\n{2}\n{3}\n{4}".format(method,
                                               req_url.path,
                                               "?" + query,
                                               head,
                                               head_list)

        request_sum = hashlib.sha256(bytearray(request_text, 'utf-8')).hexdigest()

        auth_text = "{0}\n{1}\n{2}".format(date_long,
                                        cred,
                                        request_sum)

        sig = hmac.new(bytearray(self._signing_key(date_short), 'utf-8'),
                       msg=bytearray(auth_text, 'utf-8'),
                       digestmod=hashlib.sha256).hexdigest()

        return query + "&signature={0}".format( sig )



'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

import base64
import hashlib
import hmac
from email.utils import formatdate

import requests

from sxclient.models import UserData  # noqa
from sxclient.tools.string_helpers import tobytes


class SXAuth(requests.auth.AuthBase):
    '''
    Attach custom 'Authorization' and 'Date' headers to the request;
    the headers are required for SX cluster-side request authentication.
    '''

    def __init__(self, user_data):
        # type: (UserData) -> None
        self.uid = user_data.uid
        self.secret_key = user_data.secret_key
        self.padding = user_data.padding

    def __call__(self, r):
        # type: (requests.Request) -> requests.Request
        body = tobytes(r.body or '')  # type: ignore FIXME
        bodysha1 = hashlib.sha1(body).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        request_string = b'\n'.join(map(tobytes, (
            r.method,
            r.path_url.lstrip('/'),  # type: ignore FIXME
            date,
            bodysha1,
            ''
        )))

        digest = hmac.new(
            self.secret_key, request_string, hashlib.sha1
        ).digest()
        auth_token = self.uid + digest + self.padding
        auth_token = base64.encodestring(auth_token).rstrip()
        auth_header = b'SKY ' + auth_token

        r.headers['Authorization'] = auth_header
        r.headers['Date'] = date
        return r

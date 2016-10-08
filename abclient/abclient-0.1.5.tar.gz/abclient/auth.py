#    Copyright (c) 2016 Shanghai EISOO Information Technology Corp.
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import base64
import hmac
import hashlib
import urllib2
from functools import wraps


def get_query_token(method, url, app_id, app_secret):
    decisive_element = base64.b64encode(method + url)
    signature = base64.b64encode(
        hmac.new(app_secret, decisive_element, hashlib.sha1).digest())
    query_string = ("?appid=%(appid)s&signature=%(signature)s") % {"appid": app_id,
                                                                   "signature":signature}
    return query_string

def auth(app_id, app_secret):
    '''Add EISOO AnyBackup authentication to a function send http
    request to AnyBackup server.

    :param app_id: id for authentication.Get it from AnyBackup console.
    :param app_secret: secret for authentication.Get it from AnyBackup console.
    '''

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            method = args[1]
            url = args[2]
            params = get_query_token(method, url, app_id, app_secret)
            kwargs['params'] = params
            return func(*args, **kwargs)
        return wrapper
    return decorate

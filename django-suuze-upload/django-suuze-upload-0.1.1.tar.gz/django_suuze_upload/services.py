# coding: utf-8
import json
from time import time
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests

from .utils import encode_with_base64
from .utils import decode_with_base64
from .utils import SUUZE_UPLOAD_CONFIG


TOKEN_URL = 'oauth/uptoken/'
UPLOAD_URL = 'file/upload/'


def standard_response(resp):
    if resp.status_code == 200:
        kw = json.loads(resp.text)
    elif resp.status_code < 500:
        kw = {
            'status_code': resp.status_code,
            'error': json.loads(resp.text)['error']
        }
    else:
        kw = {
            'status_code': resp.status_code,
            'error': resp.text
        }
    return kw


def is_uptoken_expire(uptoken):
    expire = decode_with_base64(uptoken.split(':')[-1])
    return int(time()) - int(expire) > 0


def fetch_uptoken():
    payload = {
        'app': SUUZE_UPLOAD_CONFIG['app'],
        'path': SUUZE_UPLOAD_CONFIG['path'],
        'access_key': encode_with_base64(SUUZE_UPLOAD_CONFIG['access_key']),
        'expire': SUUZE_UPLOAD_CONFIG.get('expire')
    }
    url = urljoin(SUUZE_UPLOAD_CONFIG['domain'], TOKEN_URL)
    try:
        resp = requests.post(url, data=payload)
    except requests.exceptions.RequestException:
        return {
            'status_code': 504,
            'error': '{} unreceivable, request timeout'.format(url)
        }

    return standard_response(resp)


def upload_file(uptoken, file_object):
    payload = {
        'app': SUUZE_UPLOAD_CONFIG['app'],
        'path': SUUZE_UPLOAD_CONFIG['path'],
        'uptoken': uptoken
    }
    files = {'file': file_object}

    url = urljoin(SUUZE_UPLOAD_CONFIG['domain'], UPLOAD_URL)
    try:
        resp = requests.post(url, data=payload, files=files)
    except requests.exceptions.RequestException:
        return {
            'status_code': 504,
            'error': '{} unreceivable, request timeout'.format(url)
        }

    return standard_response(resp)

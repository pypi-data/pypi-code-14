# coding: utf-8
import json
import base64
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

URLPATH = 'oauth/uptoken/'


def encode_with_base64(text):
    return base64.b64encode(str.encode(text))


def load_config():
    op_config = getattr(settings, 'SUUZE_UPLOAD_CONFIG', {})
    if not op_config:
        raise ImproperlyConfigured(
            "You have to define SUUZE_UPLOAD_CONFIG in settings.py")
    required_fields = ('domain', 'app', 'path', 'access_key')
    for field in required_fields:
        if field not in op_config:
            raise ImproperlyConfigured(
                "SUUZE_UPLOAD_CONFIG required {} setted".format(field))

    return op_config


def fetch_uptoken():
    conf = load_config()
    payload = {
        'app': conf['app'],
        'path': conf['path'],
        'access_key': encode_with_base64(conf['access_key']),
        'expire': conf.get('expire')
    }
    url = urljoin(conf['domain'], URLPATH)
    resp = requests.post(url, data=payload)
    if resp.status_code == 200:
        return json.loads(resp.text)

    return {'status_code': resp.status_code, 'error': resp.text}

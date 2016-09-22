# coding: utf-8
import base64
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def encode_with_base64(text):
    return base64.b64encode(str.encode(text))


def decode_with_base64(text):
    raw_bytes = base64.b64decode(text)
    return bytes.decode(raw_bytes)


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

SUUZE_UPLOAD_CONFIG = load_config()

"""
This module is imported on app ready (see __init__).
"""
from django.conf import settings
from django_memdb.signals import store_load, store_save
from cenvars import codec
from . import __info__


if settings.CENVARS_KEY is None: # pragma: no cover
    KEY = KEY_SIZE = None
else:
    _, KEY_SIZE, _, KEY = codec.decode_key(settings.CENVARS_KEY)

def persistent_crypt(**kwargs):
    "Persistent data for memdb is stored encrypted."
    # We only want to do crypto for the models in this application.
    if __info__.LABELS['name'] == kwargs['kwargs']['application']:
        data = kwargs['kwargs']['data']
        if kwargs['kwargs']['process'] == 'encode':
            data = codec.encrypt(KEY, data)
        else:
            data = codec.decrypt(KEY, data, key_size=KEY_SIZE)

        kwargs['kwargs']['data'] = data

store_load.connect(persistent_crypt)
store_save.connect(persistent_crypt)
 
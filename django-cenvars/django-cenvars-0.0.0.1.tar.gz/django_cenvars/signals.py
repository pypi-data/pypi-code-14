"""
This module is imported on app ready (see __init__).
"""
from django.conf import settings
from django_memdb.signals import store_load, store_save
from . import __info__
from .tools import codec

KEY = codec.decode_key(settings.CENVARS_KEY)[1]

def persistent_crypt(**kwargs):
    "Persistent data for memdb is stored encrypted."
    # We only want to do crypto for the models in this application.
    if __info__.LABELS['name'] == kwargs['kwargs']['application']:
        data = kwargs['kwargs']['data']
        if kwargs['kwargs']['process'] == 'encode':
            data = codec.encrypt(KEY, data)
        else:
            data = codec.decrypt(KEY, data)

        kwargs['kwargs']['data'] = data

store_load.connect(persistent_crypt)
store_save.connect(persistent_crypt)
 
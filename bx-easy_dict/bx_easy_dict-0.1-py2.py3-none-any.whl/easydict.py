# -*- coding: utf-8 -*-
from collections import Mapping

__author__ = 'banxi'


class _EasyDict(dict):
    def __init__(self, *args, **kwargs):
        self.__missing = kwargs.pop('_missing', None)
        super(_EasyDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        if item in self:
            return self[item]
        else:
            return self.__missing


def easy_dict(dct, _missing=None):
    if isinstance(dct, Mapping):
        items = [(k, easy_dict(v, _missing=_missing)) for k, v in dct.items()]
        return _EasyDict(items, _missing=_missing)
    else:
        return dct


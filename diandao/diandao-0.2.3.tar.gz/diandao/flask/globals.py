# -*- coding: utf-8 -*-

from functools import partial
from werkzeug.local import LocalStack, LocalProxy

stacker = {"app": None}

def _lookup_(name):
    return stacker[name]

app=LocalProxy(partial(_lookup_,"app"))
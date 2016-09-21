# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import logging

from timberjack import get_logger
from timberjack.configure import configure_structlog


class Timberjack(object):

    def __init__(self, app, level=logging.INFO):
        self.app = app
        self.level = level

        configure_structlog()

        logging.basicConfig(level=level)

    @classmethod
    def get_logger(name=None, *args, **kwargs):
        return get_logger(name, *args, **kwargs)

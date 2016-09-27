#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import sys
import datetime

from pysodbm import Database
from ExampleApp.Controllers.Product import Product

__author__ = 'Marco Bartel'

LOG = logging.getLogger(__name__)
LOG.level = logging.DEBUG
format = logging.Formatter('%(levelname)8s: [%(name)s] %(message)s')
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(format)
LOG.addHandler(stream_handler)
#

class ExampleAppDb(Database):
    def __init__(self):
        super(ExampleAppDb, self).__init__()


    def dbMakeConnection(self):
        return super(ExampleAppDb, self).dbMakeConnection(
            host="example.com",
            user="me",
            password="mypass",
            db="base",
        )


class ExampleApp(object):
    def __init__(self):
        products = Product.getMultipleRecordsWhere(esgento=db, whereClause="sku > 137095 limit 10")
        print products



db = ExampleAppDb()


if __name__ == '__main__':
    LOG.info("start")
    ea = ExampleApp()
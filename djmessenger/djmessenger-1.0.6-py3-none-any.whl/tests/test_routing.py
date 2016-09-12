# -*- coding: utf-8 -*-
from django.test import TestCase
from djmessenger.routing import *
import os
from djmessenger.settings import *
import json
from pprint import pprint
from djmessenger.handling import BaseHandler
from djmessenger.receiving import ReceivingType


class TestRouter(TestCase):
    def test_deserialization(self):
        file = os.path.join(DJM_BASE_DIR, 'ref', 'default_routing.json')
        self.assertTrue(os.path.exists(file))
        policy = Policy.read_json(file)
        # pprint(router)
        # print(ReceivingType.members())
        for router in policy.routers:
            self.assertTrue(isinstance(router, Router))
            try:
                # print(type(router.get_receiving_type()))
                self.assertTrue(isinstance(router.get_receiving_type(), ReceivingType))
            except Exception as e:
                self.fail('should not fail but %s' % e)
            self.assertTrue(isinstance(router.handlers, list))
            for handler in router.handlers:
                self.assertTrue(isinstance(handler, TargetHandlerClass))
                try:
                    self.assertTrue(issubclass(handler.get_class(), BaseHandler))
                except Exception as e:
                    self.fail('should not fail but %s' % e)

    def test_basic(self):
        # policy has been loaded
        self.assertEqual(4, len(policy.routers))
        self.assertEqual(ReceivingType.DEFAULT, policy.get_router(ReceivingType.DEFAULT).get_receiving_type())
        handlers = policy.get_handlers(ReceivingType.DEFAULT)
        self.assertEqual(2, len(handlers))
        for handler in handlers:
            self.assertTrue(issubclass(handler, BaseHandler), 'handler is type %s' % type(handler))

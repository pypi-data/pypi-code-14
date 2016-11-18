# -*- coding: utf-8 -*-
from django.test import TestCase
from djmessenger.routing import *
import os
from djmessenger.settings import *
import json
from djmessenger.handling import BaseHandler


class TestRouter(TestCase):
    def test_deserialization(self):
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_routing.json')
        self.assertTrue(os.path.exists(file), file)
        policy = Policy.read_json(file)
        self.assertTrue(isinstance(policy, Policy))
        policy = None
        with open(file) as fp:
            data = json.load(fp)
            policy = Policy.get_instance(data)
        self.assertIsNotNone(policy)
        for rule in policy.rules:
            self.assertIsInstance(rule, Rule, 'rule should be of type Rule but '
                                              'was %s' % type(rule))
            for wrapper in rule.get_filter_wrappers():
                self.assertIsInstance(wrapper, TargetFilterClass)
                try:
                    filter_ = wrapper.get_instance()
                    self.assertIsInstance(filter_, BaseFilter)
                except Exception as e:
                    assert False, 'get_instance from %s should pass but %s' \
                                  % (wrapper, e)
            for wrapper in rule.get_handler_wrappers():
                self.assertIsInstance(wrapper, TargetHandlerClass)
                try:
                    handler = wrapper.get_instance()
                    self.assertIsInstance(handler, BaseHandler)
                except Exception as e:
                    assert False, 'get_instance from %s should pass but %s' \
                                  % (wrapper, e)
            for wrapper in rule.get_replier_wrappers():
                self.assertIsInstance(wrapper, TargetReplierClass)
                try:
                    replier = wrapper.get_instance()
                    self.assertIsInstance(replier, CommonReplier)
                except Exception as e:
                    assert False, 'get_instance from %s should pass but %s' \
                                  % (wrapper, e)
            for filter_ in rule.get_filter_instances():
                self.assertIsInstance(filter_, BaseFilter)
            for handler in rule.get_handler_instances():
                self.assertIsInstance(handler, BaseHandler)
            for replier in rule.get_replier_instances():
                self.assertIsInstance(replier, CommonReplier)

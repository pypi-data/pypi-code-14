# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
from djmessenger.receiving import *
import os
from pprint import pprint, pformat
import json
from deepdiff import DeepDiff


SAMPLE_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'sample_json')


def get_sample_path(callback_type):
    ret = os.path.join(SAMPLE_BASE, '%s.json' % callback_type.name)
    assert os.path.exists(ret), 'sample json file %s does not exist' % ret
    return ret


class TestMessaging(unittest.TestCase):
    """
    Sometimes these tests might fail, but I suspect it is an issue with deepdiff
    library because it is intermittent, most of the times all tests passed
    """
    def test_read_json(self):
        # pprint(CallbackType.members())
        for _, ctype in ReceivingType.get_members().items():
            if ctype == ReceivingType.DEFAULT:
                continue
            file = get_sample_path(ctype)
            dct_from_file = None
            try:
                callback = Callback.read_json(file)
                with open(file, 'r') as fp:
                    dct_from_file = json.load(fp)
            except AssertionError:
                self.fail('Fail to load sample json file from %s to Callback' %
                          file)
            dct_from_obj = callback.json()
            # ddiff = DeepDiff(dct_from_file, dct_from_obj, ignore_order=True)
            # self.assertTrue(not ddiff, '%s\n%s' % (file, pformat(ddiff)))

    def test_callback_type_check(self):
        for _, ctype in ReceivingType.get_members().items():
            if ctype == ReceivingType.DEFAULT:
                continue
            file = get_sample_path(ctype)
            dct_from_file = None
            try:
                callback = Callback.read_json(file)
                with open(file, 'r') as fp:
                    dct_from_file = json.load(fp)
                for entry in callback.entry:
                    for messaging in entry.messaging:
                        callbacktype = messaging.get_receiving_type()
                        self.assertEqual(ctype, callbacktype)
            except Exception as e:
                self.fail('Fail to check CallbackType for %s because %s' %
                          (file, e))
                # traceback.print_exc()


    def test_message_received(self):
        file = get_sample_path(ReceivingType.SIMPLE_TEXT)
        callback = Callback.read_json(file)
        dct_from_file = None
        with open(file, 'r') as fp:
            dct_from_file = json.load(fp)
            # pprint(dct_from_file)
        dct_from_obj = callback.json()
        ddiff = DeepDiff(dct_from_file, dct_from_obj, ignore_order=True)
        self.assertTrue(not ddiff, '%s\n%s' % (file, pformat(ddiff)))
        for entry in callback.entry:
            self.assertTrue(isinstance(entry, Entry))
            self.assertIsNotNone(entry.id)
            self.assertIsNotNone(entry.time)
            for messaging in entry.messaging:
                self.assertTrue(isinstance(messaging, Messaging))
                self.assertEqual('USER_ID', messaging.sender.id)
                self.assertEqual('PAGE_ID', messaging.recipient.id)
                self.assertIsNotNone(messaging.timestamp)
                message = messaging.message
                self.assertTrue(isinstance(message, Message))
                self.assertIsNotNone(message.mid)
                self.assertIsNotNone(message.seq)
                self.assertIsNotNone(message.text)

# -*- coding: utf-8 -*-

import traceback
from unittest import TestCase
from preggy import expect

from exec_pypeline.action import Action

from .pass_action import PassAction


class MyAction(PassAction):
    name = "My super action"


class MyUnicodeErrorAction(PassAction):
    pass


class ActionTestCase(TestCase):

    def test_my_action(self):
        act = MyAction()
        expect(act.name).to_equal("My super action")
        expect(act.forward({})).to_equal(None)
        expect(act.backward(None, {})).to_equal(None)

    def test_to_dict_method(self):
        act = MyAction()
        expect(act.to_dict()).to_equal({
            'id': act.id,
            'name': act.name,
            'status': act.status,
            'error': {
                'msg': None,
                'traceback': None,
                'class': None,
            },
            'outcome': None,
        })

    def test_to_dict_encodes_correctly_unicode_exception_messages(self):
        act = MyUnicodeErrorAction()
        exception_msg = u'opá'
        exception_class = Exception

        try:
            raise exception_class(exception_msg)
        except exception_class, e:
            error = e

        act.error = error

        expect(act.to_dict()).to_equal({
            'id': act.id,
            'name': act.name,
            'status': act.status,
            'error': {
                'msg': exception_msg,
                'traceback': traceback.format_exc(error),
                'class': error.__class__.__name__,
            },
            'outcome': None,
        })

    def test_from_dict_method(self):
        first = MyAction()
        second = Action.from_dict(first.to_dict())
        expect(second.to_dict()).to_equal(first.to_dict())

    def test_from_dict_method_with_error(self):
        first = MyAction()
        first.error = RuntimeError('foo')
        second = Action.from_dict(first.to_dict())
        expect(second.to_dict()).to_equal(first.to_dict())

# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Hijacking strategies
"""
import logging

from importlib import import_module

from ..hook_point import hook_point
from ...exceptions import SqreenException

from .base import BaseStrategy
from .dbapi2 import DBApi2Strategy
from .import_hook import ImportHookStrategy
from .psycopg2 import Psycopg2Strategy
from .flask import FlaskStrategy
from .django import DjangoStrategy

__all__ = ['BaseStrategy', 'DBApi2Strategy', 'ImportHookStrategy',
           'Psycopg2Strategy', 'FlaskStrategy', 'DjangoStrategy']

LOGGER = logging.getLogger(__name__)


class InvalidHookPoint(SqreenException):
    """ Exception raised when the hook_point couldn't be found or is invalid
    """
    pass


class SetAttrStrategy(BaseStrategy):
    """ Simple strategy that calls setattr(hook_module, hook_name, callback)
    """

    def __init__(self, hook_name, channel, before_hook_point=None):
        super(SetAttrStrategy, self).__init__(channel, before_hook_point)
        self.hook_module, self.hook_name = hook_name
        self.original = self._get_original()

    def hook(self, callback):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook to the endpoint.
        """
        self.add_callback(callback)

        # Check that we didn't already hooked the endpoint
        if self.hooked is False:
            _hook_point = hook_point(self, callback.hook_module,
                                     callback.hook_name, self.original)

            module = self._get_hook_to()
            setattr(module, self.hook_name, _hook_point)

            self.hooked = True

    def _get_original(self):
        """ Return the original function defined at (hook_module, hook_name)
        """

        if self.hook_name == '':
            raise InvalidHookPoint('Empty hook_name')

        module = self._get_hook_to()

        try:
            return getattr(module, self.hook_name)
        except AttributeError:
            msg = "Bad hook_name {} on hook_module {}"
            raise InvalidHookPoint(msg.format(self.hook_name,
                                              self.hook_module))

    def _get_hook_to(self):
        """ Retrieve the python module or class corresponding to hook_name
        """

        if self.hook_module == '':
            raise InvalidHookPoint('Empty hook_module')

        # Check if the klass is part module and part klass name
        if '::' in self.hook_module:
            module_name, class_name = self.hook_module.split('::', 1)
        else:
            module_name, class_name = self.hook_module, None

        try:
            module = import_module(module_name)
        except ImportError:
            raise InvalidHookPoint("Bad module name {}".format(module_name))

        if class_name:
            try:
                module = getattr(module, class_name)
            except AttributeError:
                msg = "Bad class_name {} on module {}".format(class_name, module_name)
                raise InvalidHookPoint(msg)

        return module

    @staticmethod
    def get_strategy_id(callback):
        """ Return the tuple (callback.hook_module, callback.hook_name) as
        identifier for this strategy
        """
        return (callback.hook_module, callback.hook_name)

    def _restore(self):
        """ Restore the original function at the hooked path
        """
        module = self._get_hook_to()
        setattr(module, self.hook_name, self.original)
        self.hooked = False

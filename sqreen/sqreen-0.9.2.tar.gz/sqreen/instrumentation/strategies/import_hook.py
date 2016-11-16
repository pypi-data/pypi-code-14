# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Import hook strategy to prepare hooks for modules
"""
import sys
import logging

from ..helpers import partial
from ..hook_point import hook_point
from ..import_hook import ImportHook, get_hook_parent, get_hook_path

from .base import BaseStrategy

LOGGER = logging.getLogger(__name__)


class ImportHookStrategy(BaseStrategy):
    """ Simple strategy that calls setattr(hook_module, hook_name, callback)
    """

    def __init__(self, hook_name, channel, before_hook_point=None):
        super(ImportHookStrategy, self).__init__(channel, before_hook_point)
        self.hook_module = hook_name

        self.hook_points = set()

    def hook(self, callback):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook to the endpoint.
        """
        self.add_callback(callback)

        try:
            callback_module_path = callback.hook_module.split('::', 1)[1]
        except IndexError:
            callback_module_path = ''

        self.hook_points.add((callback_module_path, callback.hook_name))

        # Check that we didn't already hooked the endpoint
        if self.hooked is False:
            import_hook = ImportHook(self.hook_module, self.import_hook_callback)
            sys.meta_path.insert(0, import_hook)

            self.hooked = True

    def import_hook_callback(self, module):
        """ Monkey-patch the object located at hook_class.hook_name on an
        already loaded module. Called by ImportHook
        """

        for hook_class, hook_name in self.hook_points:
            hook_path = get_hook_path(self.hook_module, hook_class)

            # Retrieve the original
            hook_parent = get_hook_parent(module, hook_class)

            if hook_parent is None:
                msg = "'%s' doesn't exists for module %s at path '%s', couldn't hook"
                LOGGER.warning(msg, hook_class, module, hook_path)
                continue

            original = getattr(hook_parent, hook_name, None)

            # Do not create functions if original don't exists
            if original is None:
                msg = "'%s' doesn't exists for %s at path '%s'"
                LOGGER.warning(msg, hook_name, hook_parent, hook_path)
                continue

            # Hook it
            _hook_point = hook_point(self, hook_path,
                                     hook_name, original)

            # And replace it
            setattr(hook_parent, hook_name, _hook_point)
            LOGGER.debug("Successfully hooking on %s %s", hook_path,
                         hook_name)

        return module

    @staticmethod
    def get_strategy_id(callback):
        """ Return the tuple (callback.hook_module, callback.hook_name) as
        identifier for this strategy
        """
        return callback.hook_module.split('::', 1)[0]

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass

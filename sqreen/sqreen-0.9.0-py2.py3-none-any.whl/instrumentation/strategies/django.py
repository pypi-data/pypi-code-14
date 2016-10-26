# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Django hook strategy
"""

import sys

from logging import getLogger

from .base import BaseStrategy
from ..hook_point import DjangoMiddleware
from ..import_hook import ImportHook, get_hook_parent


LOGGER = getLogger(__name__)


def load_middleware_insert(original, middleware):

    def wrapped_load_middleware(self, *args, **kwargs):
        LOGGER.debug("Execute load_middleware_insert")

        # Load original middlewares
        result = original(self, *args, **kwargs)

        # Insert out custom one
        try:
            self._view_middleware.insert(0, middleware.process_view)
            self._response_middleware.append(middleware.process_response)
            self._exception_middleware.append(middleware.process_exception)
        except Exception:
            LOGGER.warning("Error while inserting our middleware", exc_info=True)

        return result

    return wrapped_load_middleware


class DjangoStrategy(BaseStrategy):
    """ Strategy for Django peripheric callbacks.

    It injects a custom DjangoFramework that calls callbacks for each
    lifecycle method
    """

    MODULE_NAME = "django.core.handlers.base"
    HOOK_CLASS = "BaseHandler"
    HOOK_METHOD = "load_middleware"

    def __init__(self, strategy_key, channel, before_hook_point=None):
        super(DjangoStrategy, self).__init__(channel, before_hook_point)
        self.strategy_key = strategy_key

        self.django_middleware = DjangoMiddleware(self, channel)

        self.hooked = False

    def hook(self, callback):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook the load_middleware to insert our
        middleware.

        Once hooked, the middleware will call the callbacks at the right moment.
        """
        # Register callback
        self.add_callback(callback)

        # Check if we already hooked at
        if not self.hooked:

            import_hook = ImportHook(self.MODULE_NAME, self.import_hook_callback)
            sys.meta_path.insert(0, import_hook)

            self.hooked = True

    def import_hook_callback(self, module):
        """ Monkey-patch the object located at hook_class.hook_name on an
        already loaded module
        """
        hook_parent = get_hook_parent(module, self.HOOK_CLASS)

        original = getattr(hook_parent, self.HOOK_METHOD, None)
        hooked = load_middleware_insert(original, self.django_middleware)
        setattr(hook_parent, self.HOOK_METHOD, hooked)
        LOGGER.debug("Successfully hooked on %s %s", self.MODULE_NAME,
                     self.HOOK_CLASS)

    @classmethod
    def get_strategy_id(cls, callback):
        """ This strategy only hook on
        (django.core.handlers.base::BaseHandler, load_middleware)
        """
        return ("{}::{}".format(cls.MODULE_NAME, cls.HOOK_CLASS), cls.HOOK_METHOD)

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass

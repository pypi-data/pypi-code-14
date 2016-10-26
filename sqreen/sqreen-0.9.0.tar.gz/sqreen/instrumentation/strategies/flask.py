# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Flask hook strategy
"""

import sys

from logging import getLogger

from .base import BaseStrategy
from ..hook_point import FlaskMiddleware
from ..import_hook import ImportHook, get_hook_parent


LOGGER = getLogger(__name__)


def try_trigger_before_first_request_functions_wrapper(original, middleware):

    def wrapped_try_trigger_before_first_request_functions(self, *args, **kwargs):
        LOGGER.debug("Execute try_trigger_before_first_request_functions_wrapper")

        try:
            # Ensure we insert our middleware only once
            if self._got_first_request is False:
                # Insert pre middleware method
                self.before_request_funcs.setdefault(None, []).insert(0, middleware.pre)

                # Insert post middleware method
                self.after_request_funcs.setdefault(None, []).insert(0, middleware.post)
        except Exception:
            LOGGER.warning("Error while inserting our middleware", exc_info=True)

        return original(self, *args, **kwargs)

    return wrapped_try_trigger_before_first_request_functions


class FlaskStrategy(BaseStrategy):
    """ Strategy for Flask peripheric callbacks.

    It injects functions that calls pre and post callbacks in the Flask
    request workflow
    """

    MODULE_NAME = "flask.app"
    HOOK_CLASS = "Flask"
    HOOK_METHOD = "try_trigger_before_first_request_functions"

    def __init__(self, strategy_key, channel, before_hook_point=None):
        super(FlaskStrategy, self).__init__(channel, before_hook_point)
        self.strategy_key = strategy_key

        self.flask_middleware = FlaskMiddleware(self, channel)

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
        hooked = try_trigger_before_first_request_functions_wrapper(original, self.flask_middleware)
        setattr(hook_parent, self.HOOK_METHOD, hooked)
        LOGGER.debug("Successfully hooked on %s %s", self.MODULE_NAME,
                     self.HOOK_CLASS)

    @classmethod
    def get_strategy_id(cls, callback):
        """ This strategy only hook on
        flask.app::Flask, try_trigger_before_first_request_functions)
        """
        return ("{}::{}".format(cls.MODULE_NAME, cls.HOOK_CLASS), cls.HOOK_METHOD)

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass

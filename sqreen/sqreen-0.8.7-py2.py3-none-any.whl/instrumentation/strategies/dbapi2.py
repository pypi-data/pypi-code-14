# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" DBApi2 strategy and custom connection and cursor classes
"""
import sys
import logging
import inspect

from ..helpers import partial, Proxy
from ..hook_point import hook_point
from ..import_hook import ImportHook
from ...utils import update_wrapper

from .base import BaseStrategy


LOGGER = logging.getLogger(__name__)


class CustomCursor(Proxy):
    """ CustomCursor proxy, it proxy a real Cursor of a DBApi2
    module, instrument all methods with prefix ::Cursor.
    """

    def __init__(self, real_cursor, hook_point, module_path):
        super(CustomCursor, self).__init__(real_cursor)

        methods = inspect.getmembers(self._obj, inspect.ismethod)
        builtins = inspect.getmembers(self._obj, inspect.isbuiltin)

        for method in methods + builtins:
            if method[0].startswith('_'):
                # Ignore private or semi-private methods
                continue

            hook_module = "{}::Cursor".format(module_path)
            new_hook_point = hook_point(hook_module, method[0],
                                        method[1])
            object.__setattr__(self, method[0], new_hook_point)


class CustomConnection(Proxy):
    """ CustomConnection proxy, it proxy a real Connection of a DBApi2
    module, instrument all methods with prefix ::Connection and returns
    CustomCursor when callin the cursor method.
    """

    def __init__(self, real_connection, hook_point, module_path):
        self._sqreen_hook_point = hook_point
        self._sqreen_module_path = module_path
        super(CustomConnection, self).__init__(real_connection)

        methods = inspect.getmembers(self._obj, inspect.ismethod)
        builtins = inspect.getmembers(self._obj, inspect.isbuiltin)

        for method in methods + builtins:
            if method[0] == 'cursor':
                # Don't hook on cursor
                continue

            if method[0].startswith('_'):
                # Ignore private or semi-private methods
                continue

            hook_module = "{}::Connection".format(module_path)
            new_hook_point = hook_point(hook_module, method[0], method[1])
            object.__setattr__(self, method[0], new_hook_point)

    def cursor(self, *args, **kwargs):
        """ Instantiate a real cursor, proxy it via CustomCursor.
        """
        return CustomCursor(self._obj.cursor(*args, **kwargs),
                            self._sqreen_hook_point, self._sqreen_module_path)


def custom_connect(hook_point, module_path, original_connect, *args, **kwargs):
    """ Replacement to the connect function of a DBApi2 module. It will
    instantiate a connection via the original connect function and proxy it
    via CustomConnection defined earlier.
    """

    def wrapper(*args, **kwargs):
        return CustomConnection(original_connect(*args, **kwargs), hook_point, module_path)

    wrapper = update_wrapper(wrapper, original_connect)
    return wrapper


class DBApi2Strategy(BaseStrategy):
    """ Strategy for DBApi2 drivers.

    It's different from the SetAttrStrategy and requires special care in
    hook_module and hook_name.
    DBApi2 tries to hook on 'connect' method of DBApi2 compatible driver.
    In order to do so, it needs the module name where 'connect' is available. It
    must be the first part of hook_module, for example in sqlite3, it will be
    'sqlite3'.

    The hook_module could then contains either '::Cursor' for hooking on
    cursor methods or '::Connection' for hooking on connection methods.
    The hook_name will then specify which method it will hook on.

    For example with sqlite3, the tuple ('sqlite3::Connection', 'execute') will
    reference the execute method on a sqlite3 connection.
    In the same way, the tuple ('sqlite3::Cursor', 'execute') will reference
    the execute method on a sqlite3 cursor.

    It will works the same way for all DBApi2 drivers, even with psycopg2
    where cursor class is actually defined as 'psycopg2.extensions.cursor',
    'psycopg2::Cursor' will correctly reference all psycopg2 cursor methods.
    """

    def __init__(self, module_path, channel, before_hook_point=None):
        super(DBApi2Strategy, self).__init__(channel, before_hook_point)
        self.module_path = module_path

        self.hooked = False

    def hook(self, callback):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook to the endpoint.

        Once hooked, it will instrument all method on connection and cursor.
        But if no callback is defined on a specific method, the overhead will
        be minimal.
        """
        # Register callback
        self.add_callback(callback)

        # Check if we already hooked at
        if not self.hooked:

            import_hook = ImportHook(self.module_path, self.import_hook_callback)
            sys.meta_path.insert(0, import_hook)

            self.hooked = True

    def import_hook_callback(self, module):
        """ Monkey-patch the object located at hook_class.hook_name on an
        already loaded module
        """
        original = getattr(module, "connect", None)

        if original is None:
            msg = "'%s' doesn't exists for module %s at path '%s', couldn't hook"
            LOGGER.warning(msg, 'connect', module, self.module_path)
            return

        _hook_point = partial(hook_point, self)
        new_connect = custom_connect(_hook_point, self.module_path, original)
        setattr(module, "connect", new_connect)
        LOGGER.debug("Successfully hooking on %s %s", self.module_path,
                     "connect")

    @staticmethod
    def get_strategy_id(callback):
        """ Returns the module part of hook_module (without everything after
        ::) as identifier for this strategy. Multiple hooks on sqlite3* should
        be done in this strategy.
        """
        # Check if the klass is part module and part klass name
        if '::' in callback.hook_module:
            return callback.hook_module.split('::', 1)[0]
        else:
            return callback.hook_module

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass

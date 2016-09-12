# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Import hook related helpers
"""
import sys
import imp
import logging

LOGGER = logging.getLogger(__name__)


def get_hook_parent(module, hook_class):
    """ From a module, its name and a class, retrieve the right class
    and returns both the hook parent and the full hook path
    """
    if hook_class:
        if '.' in hook_class:
            raise NotImplementedError()
        else:
            return getattr(module, hook_class, None)
    else:
        return module


def get_hook_path(hook_module, hook_class):
    """ Return the full hook path from hook_module and potentially None hook_class
    """
    if hook_class:
        return '{}::{}'.format(hook_module, hook_class)
    else:
        return hook_module


class ImportHook(object):
    """ Custom import hook that import a module and hook on several
    hook points of this module
    """

    def __init__(self, module_name, hook_callback):
        self.module_name = module_name
        self.hook_callback = hook_callback
        self.executing = False
        self.path = None

        # If modules was already imported, try to hook on them
        if self.module_name in sys.modules:
            msg = "Module %s was already imported, hooking now"
            LOGGER.warning(msg, self.module_name)
            self.hook_callback(sys.modules[self.module_name])

    def find_module(self, fullname, path=None):
        """ Check if loading module name match the one we want
        """
        if fullname == self.module_name:
            self.path = path
            return self
        return

    def load_module(self, name):
        """ Import and hook the module
        """
        LOGGER.debug("Trying to monkey-patch module %s", name)
        # Hierachical import
        module = self._load_module(name, self.path)

        try:
            self.hook_callback(module)
        except Exception:
            err_msg = "Error while hooking on module %s"
            LOGGER.warning(err_msg, self.module_name, exc_info=True)
        finally:
            sys.modules[name] = module
            return module

    @staticmethod
    def _load_module(name, path):
        """ Load a module without putting it in sys.modules
        """
        if name in sys.modules:
            LOGGER.warning("Module %s was already imported", name)
            return sys.modules[name]
        else:
            splitted_name = name.split('.')

            submodule = None

            # The algorithm for loading path inside a package
            # is to load the package first then the subpackage until to the
            # module.
            # find_module take the package name, eg: 'app' for flask.app
            # load_module take the full name, eg 'flask.app' for flask.app
            for index, part in enumerate(splitted_name):
                subpath = '.'.join(splitted_name[:index + 1])

                if subpath in sys.modules:
                    submodule = sys.modules[subpath]
                else:
                    src_file = None
                    try:
                        src_file, pathname, description = imp.find_module(part, path)
                        submodule = imp.load_module(subpath, src_file, pathname,
                                                    description)
                    finally:
                        if src_file:
                            src_file.close()

                path = getattr(submodule, '__path__', None)

            return submodule

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.module_name,
                               self.hook_callback)

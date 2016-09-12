# -*- coding: utf-8 -*-
import importlib
import logging


logger = logging.getLogger(__name__)


def load_class(fullyname):
    """Load class by its fully qualified name

    @param fullyname: if given fully qualified name is a.b.c, try to load the
                      module from a.b and load the class c in a.b module
    @return: A class
    @raise ImportError: not able to load module
    @raise AttributeError: not able to load class
    """
    tokens = fullyname.split('.')
    # if len(tokens) == 1, then it is a module, raise exception
    if len(tokens) == 1:
        raise ValueError('The fully qualified name you gave was %s which can '
                         'not represent a class but a module' % fullyname)
    else:
        class_name = tokens.pop()
        module_name = '.'.join(tokens)

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        logger.error('Not able to import module named %s' % module_name)
        raise e
    try:
        ret = getattr(module, class_name)
    except AttributeError as e:
        logger.error('Not able to get class %s from module %s' %
                     (class_name, module_name))
        raise e
    return ret


def get_class_name(obj):
    """
    Given a type of an instance, return its fully qualified class name

    @param obj:
    @type obj: type or object
    @return: fully qualified class name
    @rtype: str
    """
    if not isinstance(obj, type):
        raise ValueError('Given class must be a type')
        return '%s.%s' % (obj.__module__, obj.__name__)
    else:
        return '%s.%s' % (obj.__module__, obj.__class__.__name__)

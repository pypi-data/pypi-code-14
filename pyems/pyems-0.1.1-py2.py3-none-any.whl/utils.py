import logging
from functools import wraps
from importlib import import_module

logger = logging.getLogger(__name__)


class EvoStreamException(Exception):
    pass


def get_module_class(class_path):
    """
    imports and returns module class from ``path.to.module.Class``
    argument
    """
    mod_name, cls_name = class_path.rsplit('.', 1)

    try:
        mod = import_module(mod_name)
    except ImportError as ex:
        raise EvoStreamException('Error importing module %s: '
                                 '"%s"' % (mod_name, ex))

    return getattr(mod, cls_name)


def expected(*expected_keys):
    expected_keys = set(expected_keys)

    def command_decorator(func):
        def wrapped_func(*args, **kwargs):
            unexpected = set(kwargs.keys()) - expected_keys

            if bool(unexpected):
                unexpected = ', '.join([key for key in list(unexpected)])
                logger.warning('Function %s: Unexpected argument(s): %s',
                               func.__name__, unexpected)

            kwargs = dict((key, val) for key, val in kwargs.items()
                          if key in expected_keys)

            return func(*args, **kwargs)

        return wraps(func)(wrapped_func)

    return command_decorator

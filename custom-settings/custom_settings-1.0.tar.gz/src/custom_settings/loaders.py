# -*- coding: utf-8 -*-
import six
from zope.dottedname import resolve

from . import (
    adapters,
    exc,
)


def load(maybe_dotted, *args, **kwds):
    if isinstance(maybe_dotted, six.string_types):
        try:
            obj = resolve.resolve(maybe_dotted)
        except ImportError:
            raise exc.NoCustomSettingModuleError(
                'Cannot import custom settings module: {}'.format(
                    maybe_dotted))
    else:
        obj = maybe_dotted
    return adapters.CustomSettings(obj, *args, **kwds)

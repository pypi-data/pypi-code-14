# -*- coding: utf-8 -*-
import os

from . import (
    exc,
    utils,
)


class CustomSettings(object):
    def __init__(
            self, data, type_=utils.NoSet, default=utils.NoSet,
            use_environ=utils.NoSet, raise_exception=utils.NoSet):
        self.data = data

        self.type_ = type_
        self.default = default
        self.use_environ = use_environ
        self.raise_exception = raise_exception

    def get(self, name, type_=utils.NoSet, default=utils.NoSet,
            use_environ=utils.NoSet, raise_exception=utils.NoSet):
        type_ = utils.coerce(type_, self.type_)
        default = utils.coerce(default, self.default)
        use_environ = utils.coerce(use_environ, self.use_environ)
        raise_exception = utils.coerce(raise_exception, self.raise_exception)

        value = getattr(self.data, name, utils.NoSet)
        if value is utils.NoSet and use_environ:
            value = os.environ.get(name, utils.NoSet)

        if value is not utils.NoSet and type_ is not None:
            try:
                value = type_(value)
            except (TypeError, ValueError) as err:
                raise exc.CustomSettingTypeError(
                    'Invalid type: {}'.format(err))

        if value is utils.NoSet and raise_exception:
            raise exc.NoCustomSettingError('Not been set: {}'.format(name))

        if value is utils.NoSet:
            value = default

        return value

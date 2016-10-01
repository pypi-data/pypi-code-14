#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re

from voluptuous import (Schema,
                        Invalid,
                        message,
                        UrlInvalid)

from karellen.stack.core import url


@message("must be either an absolute or a relative well-formed URL", cls=UrlInvalid)
def UrlValidator(v):
    try:
        v = url(v)
        if not ((v.scheme and v.netloc) or (v.scheme and v.path) or (not v.scheme and v.netloc) or (
                    not v.scheme and v.path)):
            raise ValueError
        return v
    except:
        raise ValueError from None


class ElementInvalid(Invalid):
    pass


class IterableValidator:
    """
    Validator for iterable objects
    """

    def __init__(self, validator, **kwargs):
        self.validators = validator
        self.msg = kwargs.pop('msg', None)
        self._schema = Schema(validator, **kwargs)

    def __call__(self, val):
        if not isinstance(val, (list, tuple)):
            raise Invalid("not a list or tuple")
        result = []
        try:
            for idx, v in enumerate(tuple(val)):
                result.append(self._schema(v))
        except Invalid:
            raise
        except:
            raise ElementInvalid(self.msg or 'no valid value found')
        return result if isinstance(val, list) else tuple(result)


class List(IterableValidator):
    pass


class Include:
    def __init__(self, *args, **kwargs):
        self._url = UrlValidator(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._url(*args, **kwargs)


class IdName:
    PATTERN = re.compile(r'^\s*([a-zA-Z]+[a-zA-Z0-9_]*)\s*$')

    def __init__(self, msg=None):
        self.msg = msg

    def __call__(self, v, *args, **kwargs):
        try:
            match = IdName.PATTERN.match(v)
        except TypeError:
            raise Invalid("expected string or buffer")
        if not match:
            raise Invalid(self.msg or "invalid ID name %s" % v)
        return match.group(1)

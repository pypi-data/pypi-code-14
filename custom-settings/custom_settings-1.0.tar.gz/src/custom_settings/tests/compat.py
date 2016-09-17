# -*- coding: utf-8 -*-
import six

if six.PY2:  # pragma: no cover
    import mock  # noqa
elif six.PY3:  # pragma: no cover
    from unittest import mock  # noqa

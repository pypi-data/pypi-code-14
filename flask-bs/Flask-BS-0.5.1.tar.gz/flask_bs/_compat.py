# -*- coding: utf-8 -*-
"""
    Flask-BS - Another flask extension that provides Bootstrap CSS, JS and HTML5 boilerplate.

    Author: Bill Schumacher <bill@servernet.co>
    License: LGPLv3
    Copyright: 2016 Bill Schumacher, Cerebral Power
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.
"""
import sys
"""
    Shamelessly copied from: flask_login._compat  (https://github.com/maxcountryman/flask-login) See LICENSE
    -------------------
    A module providing tools for cross-version compatibility.
"""


PY2 = sys.version_info[0] == 2


if not PY2:  # pragma: no cover
    unicode = str  # needed for pyflakes in py3


if PY2:  # pragma: nocover

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    text_type = unicode

else:  # pragma: nocover

    def iteritems(d):
        return iter(d.items())

    def itervalues(d):
        return iter(d.values())

    text_type = str


__all__ = [
    'PY2',
    'unicode',
    'iteritems',
    'itervalues',
    'text_type',
]

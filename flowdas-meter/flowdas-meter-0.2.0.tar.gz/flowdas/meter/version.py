# coding=utf-8
# Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the GNU Affero General
# Public License, v. 3.0. If a copy of the AGPL was not distributed with
# this file, You can obtain one at https://www.gnu.org/licenses/agpl-3.0.html.
from pkg_resources import get_distribution

__author__ = u'오동권(Dong-gweon Oh) <prospero@flowdas.com>'
__version__ = getattr(get_distribution('flowdas-meter'), 'version', None)

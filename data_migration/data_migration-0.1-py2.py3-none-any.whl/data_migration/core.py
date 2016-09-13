# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------

from b3j0f.conf import Configurable

@Configurable(paths = [])#decorator which get paths define in conf file.
#those files can be in several folder.
class Schema(object):

    def __init__(self, path, *args, **kwargs):

        super(Schema, self).__init__(*args, **kwargs)

        self.path = path

        self._rsc = self.getresource(path)

    def getresource(self, path):

        raise NotImplementedError()

    #valid schema independently of language.
    def validate(self, data):

        raise NotImplementedError()

    #take key in argument and make Schema.get(key) dictionary methode
    def __getitem__(self, key):

        raise NotImplementedError()

    #take key in argument and make Schema[key] = value dictionary methode
    def __setitem__(self, key, value):

        raise NotImplementedError()

    #take key in argument and make del Schema[key] dictionary methode
    def __delitem__(self, key):

        raise NotImplementedError()

    def save(self, path=None):

        if path is None:
            path = self.path

        raise NotImplementedError()

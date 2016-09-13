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

import urlparse
import os


class MigrationFactory(object):
    """instanciate the behavior class with the URL protocol
    take URI in parameter
    URI = protocol(*://)domain name(*.*.com)path(/...)"""

    def __init__(self):
        self.URL = {}

    def get(self, URI):
        protocol = get_protocol(URI)
        return self.URL[protocol.lower()]

    #on retourne cls() pour pouvoir utiliser register en tant que décorateur
    def register(self, protocol, cls):
        self.URL[protocol.lower()] = cls()
        return cls()

GLOBALFACTORY = MigrationFactory()

class MetaMigration(type):
    """MetaMigration is a metaclass
    it will be writting in URL for every class using it"""

    def __init__(cls, protocol, bases, dict):
        type.__init__(cls, protocol, bases, dict)
        GLOBALFACTORY.register(protocol, cls)


class IOInterface(object):
    """abstract class to describe function behavior
    of the different Input and Output for migration"""

    __metaclass__ = MetaMigration

    def load(self, URL):
        raise NotImplementedError()

    def transformation(self, data, transfo_cls, schema_cls):
        result = transfo_cls.apply_patch(data)
        schema_cls.validate(result)
        return result

    def save(self, result, URL):
        raise NotImplementedError()


class File(IOInterface):
    """describe load and save functions for file protocol"""

    def load(self, URL, schema):

        data = schema.getresource(get_path(URL))
        schema.validate(data)
        return data

    def save(self, result, URL, schema):

        schema.save(result, get_path(URL))


class Folder(IOInterface):
    """describe load and save functions for folder protocol"""

    def load(self, URL, schema):

        dirs = os.path.listdir(get_path(URL))
        for files in dirs :

            if os.path.isfile(files):
                data = schema.getresource(get_path(URL))
                schema.validate(data)
                return data

            elif os.path.isdir(files):
                path = os.path.join(get_path(URL), files)
                return load(self, path, schema)

            else:
                raise Exception('No such file or directory')

    def save(self, result, URL, schema):

        name = result['name']
        path = os.path.join(get_path(URL), name)
        schema.save(result, path)


class Dict(IOInterface):
    """describe load and transformation for dict protocol"""

    def load(self, URL, schema):
        data = schema.getresource(get_path(URL))
        schema.validate(data)
        return data

    def transformation(self, data, transfo_cls, schema):
        result = transfo_cls.apply_patch(data)
        schema.validate(result)
        print result


class Storage(IOInterface):
    """describe load and save functions for storage protocol"""

    def __init__(self):
        super (middleware_uri, self).__init__()

        self.storage = middleware_uri

    def load(self, URL, schema):
        data = self.storage.get_elements(id=schema['id'])
        return data

    def save(self, result, URL):
        self.storage.put_elements(result, id=result['id'])


def get_protocol(URI):
    """This function take the protocol of the URI in parameter
    and return it"""
    uri = urlparse.urlsplit(URI)
    protocol = uri[0]

    return protocol

def get_path(url):
    """This function take the path from uri in parameter
    and return it"""
    uri = urlparse.urlsplit(url)
    path = uri[2]

    return path
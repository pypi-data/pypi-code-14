from canopsis.middleware.core import Middleware
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

        try:
            return self.URL[protocol.lower()]

        except KeyError:
            for proto in self.URL:
                if protocol.lower().startswith(proto):
                    return self.URL[protocol.lower()]

            else:
                raise KeyError('No IOFacftory found for {0}'.format(URI))

    #on retourne cls() pour pouvoir utiliser register en tant que decorateur
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

        for protocol in cls.__protocols__:
            GLOBALFACTORY.register(protocol, cls)


class IOInterface(object):
    """abstract class to describe function behavior
    of the different Input and Output for migration"""

    __metaclass__ = MetaMigration

    __protocols__ = []

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

    __protocols__ = ['mongodb', 'influxdb']

    def load(self, url, schema, query=None):
        midurl = '{0}://'.format(get_path(url)[1:])
        midargs = get_params(url)

        mystorage = Middleware.get_middleware_by_uri(midurl, **midargs)

        #mystorage.connect

        cursor = mystorage.find_elements(query=query)

        return list(cursor)

    def save(self, result, url):
        midurl = '{0}://'.format(get_path(url)[1:])
        midargs = get_params(url)

        mystorage = Middleware.get_middleware_by_uri(midurl, **midargs)
        mystorage.put_elements(result)#~, _id=result['id'])


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

def get_params(url):
    """This function take the params from uri in parameter
    and return it"""
    uri = urlparse.urlsplit(url)
    params = uri[3]

    return dict(urlparse.parse_qsl(params))

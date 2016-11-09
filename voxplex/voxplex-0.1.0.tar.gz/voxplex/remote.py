import posixpath

import requests
from pyquery import PyQuery as PQ


def remote_from_config(config, name):
    remote_names = remote_names_from_config(config)
    assert name in remote_names, 'Please select from {}'.format(remote_names)
    return SunVoxRemote(name)


def remote_names_from_config(config):
    return set(d['remote'] for d in config if 'remote' in d)


class SunVoxResource(object):

    def __init__(self, remote, path):
        self.remote = remote
        while path.endswith('/'):
            path = path[:-1]
        self.path = path

    def __repr__(self):
        return '<{0.__class__.__name__} {0.path}>'.format(self)

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other):
        return self.path < other.path

    @property
    def basename(self):
        return posixpath.basename(self.path)

    @property
    def dirname(self):
        return posixpath.dirname(self.path)

    @property
    def remove_url(self):
        remove_path = '{}/?R{}'.format(self.dirname, self.basename)
        return self.remote.url_for_path(remove_path)

    def remove(self):
        requests.get(self.remove_url)


class SunVoxFile(SunVoxResource):

    is_dir = False
    is_file = True

    @property
    def url(self):
        return self.remote.url_for_path(self.path)

    def content(self):
        return requests.get(self.url).content

    def copy_to(self, local_dir):
        local_dir.write_file(self.basename, self.content())


class SunVoxDir(SunVoxResource):

    is_dir = True
    is_file = False

    @property
    def children(self):
        for child_name in self.remote.names_in_path(self.path):
            if child_name.startswith('.') or child_name.startswith('/'):
                continue
            child_path = posixpath.join(self.path, child_name)
            resource_type = \
                SunVoxDir if child_path.endswith('/') else SunVoxFile
            yield resource_type(self.remote, child_path)

    @property
    def url(self):
        return self.remote.url_for_path(self.path) \
               + ('/' if self.path != '' else '')

    def mkdir(self, name):
        response = requests.get(self.url, params={'d': name})
        assert response.ok
        return SunVoxDir(self.remote, posixpath.join(self.path, name))

    def remove(self):
        pass

    def write_file(self, basename, f):
        files = {'f1': (basename, f)}
        response = requests.post(self.url, files=files)
        assert response.ok
        return SunVoxFile(self.remote, posixpath.join(self.path, basename))


class SunVoxRemote(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<SunVoxRemote {}>'.format(self.name)

    @property
    def hostname(self):
        return '{}.local'.format(self.name)

    def all_resources(self, top='/'):
        while top.startswith('/'):
            top = top[1:]
        root = SunVoxDir(self, top)
        paths_to_get = [root]
        while len(paths_to_get) > 0:
            path = paths_to_get.pop()
            yield path
            for child in path.children:
                if child.is_dir:
                    paths_to_get.append(child)
                elif child.is_file:
                    yield child

    def dir(self, path):
        return SunVoxDir(self, path)

    def names_in_page(self, doc):
        hrefs = {a.attrib['href'] for a in doc('a')}
        names = {href for href in hrefs if not href.startswith('?')}
        return names

    def names_in_path(self, path):
        return self.names_in_page(self.page_for_path(path))

    def page_for_path(self, path):
        url = self.url_for_path(path)
        url += '/' if not url.endswith('/') else ''
        response = requests.get(url)
        doc = PQ(response.content)
        return doc

    def url_for_path(self, path):
        return 'http://{}:8080/{}'.format(self.hostname, path)

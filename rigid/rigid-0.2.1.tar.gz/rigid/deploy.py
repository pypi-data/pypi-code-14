import os
import tempfile
from rigid.utils import ObservedFileWrapper

import requests

from rigid.file_scanner import scan, tar, Skipper


class Deploy(object):
    def __init__(self, client, source):
        self.client = client
        self.source = source

    def collect_files(self):
        ignore_file = '.rignore'
        ignore_path = os.path.join(self.source, ignore_file)

        if os.path.exists(ignore_path):
            skipper = Skipper.open(ignore_path)
            skipper.rules.append(ignore_file)
        else:
            skipper = Skipper([])

        return list(filter(skipper, scan(self.source)))

    def create_tarball(self, path):
        tar(path, self.collect_files(), self.source)

    def validate(self, app):
        response = self.client.session.head(self.client.url('apps', app))
        self.client.validate(response)

    def create_source(self):
        response = self.client.session.post(self.client.url('sources'))
        self.client.validate(response)
        payload = response.json()
        return (payload['uuid'], payload['upload'])

    def upload_source(self, method, url, path, updater):
        with open(path, 'rb') as fd:
            fd = ObservedFileWrapper(fd, updater)
            response = requests.request(method, url, data=fd)
            response.raise_for_status()

    def create_version(self, url, source_uuid):
        response = self.client.session.post(url, json={'source': source_uuid})
        self.client.validate(response)
        json = response.json()
        return (json['uuid'])

    # API

    def upload(self, app):
        fd = tempfile.NamedTemporaryFile()
        self.create_tarball(fd.name)
        source_uuid, source_upload = self.create_source()
        size = os.fstat(fd.fileno()).st_size

        def func(updater):
            self.upload_source(source_upload['method'], source_upload['url'], fd.name, updater)
            fd.close()
            return source_uuid

        return (func, size)

    def upload_version(self, app, source_uuid):
        url = self.client.url('apps', app, 'versions')
        version_uuid = self.create_version(url, source_uuid)
        return version_uuid

#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

from importlib.util import spec_from_file_location
from importlib.abc import Finder, Loader
import sys
import os
import json
import shutil
import atexit
import tempfile

import requests

BASE_MODULES_DIR = tempfile.mkdtemp(prefix='singlefile')


@atexit.register
def delete_base_modules_dir():
    shutil.rmtree(BASE_MODULES_DIR, ignore_errors=True)


class GistImporter(Finder, Loader):

    __service_name__ = 'test'

    def __init__(self):
        self.path = None

    def module_repr(self, module):
        return super(self).module_repr(module)

    def find_module(self, fullname, path=None):
        self.path = path
        if fullname.startswith('singlefile.gist'):
            return self
        return None

    @staticmethod
    def is_gist(path):
        if len(path) < 3:
            return False
        return all([
            path[0] == 'gist',
            path[1].startswith('gist'),  # gist_id
            len(path[2]) > 0
        ])

    @staticmethod
    def download_file_from_gist(path, gist_id, file):
        response = requests.get('https://api.github.com/gists/{gist_id}'.format(gist_id=gist_id))
        if response.status_code == 404:
            raise ImportError('gist not found')
        if response.status_code != 200:
            raise ImportError('failed to download gist. response status code is %d' % response.status_code)
        data = json.loads(response.content.decode('utf-8'))
        if file not in data['files']:
            raise ImportError('file not found in this gist.')
        with open(path, 'w') as out:
            out.write(data['files'][file]['content'])

    @staticmethod
    def _fill_dirs(base, dirs):
        path = os.path.join(base, *dirs)
        if not os.path.exists(path):
            os.makedirs(path)
        curpath = base
        for dir in dirs:
            curpath = os.path.join(curpath, dir)
            # touch __init__.py
            open(os.path.join(curpath, '__init__.py'), 'a').close()
        try:
            if GistImporter.is_gist(dirs):
                GistImporter.download_file_from_gist(os.path.join(path, '__init__.py'), dirs[1][4:], dirs[2] + '.py')
        except ImportError as err:
            # this will ensure that the directory structure that we created will be removed
            # because if we allow that directory structure to exist, then we may never get control
            # over those erroneous import statements, because
            shutil.rmtree(path)
            raise err

    def load_module(self, fullname):
        # fullname.startswith('singlefile.gist.') is always true
        path = os.path.join(BASE_MODULES_DIR, *fullname.split('.')[1:])
        GistImporter._fill_dirs(BASE_MODULES_DIR, fullname.split('.')[1:])
        spec = spec_from_file_location(fullname, location=os.path.join(path, '__init__.py'))
        if spec is None:
            raise ImportError('spec came out as None')
        if spec.loader is None:
            raise ImportError('spec.loader came out as None')
        return spec.loader.load_module()

sys.meta_path.append(GistImporter())

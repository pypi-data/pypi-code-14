# Copyright 2016 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
from functools import partial
from itertools import chain

from gettext import NullTranslations

from piglet.exceptions import TemplateNotFound
from piglet.template import HTMLTemplate, Template

ustr = type(u'')


class TemplateLoader(object):
    """
    Loads template from the specified file system search path
    """
    def __init__(self,
                 search_path,
                 auto_reload=False,
                 default_encoding='UTF-8',
                 template_cls=HTMLTemplate,
                 translations_factory=NullTranslations,
                 cache_dir=None,
                 ):
        """
        :param search_path: a list of paths to be searched for template files;
                            or a single path
        :param auto_reload: If ``True`` the template file modification time
                            will be checked on each call to load, and the
                            template reloaded if it appears to have changed.
        :param default_encoding: The default character encoding to assume
        """
        self.search_path = search_path

        if isinstance(self.search_path, (str, ustr)):
            self.search_path = [self.search_path]

        self.auto_reload = auto_reload
        self.default_encoding = default_encoding
        self.template_cls = template_cls
        self.translations_factory = translations_factory
        self._cache = {}
        if cache_dir:
            import diskcache
            try:
                os.makedirs(cache_dir)
            except OSError:
                pass
            self._persistent_cache = diskcache.Cache(cache_dir)
        else:
            self._persistent_cache = None

    def load(self,
             filename,
             relative_to=None,
             encoding=None,
             normpath=os.path.normpath,
             isabs=os.path.isabs,
             dirname=os.path.dirname,
             relpath=os.path.relpath,
             template_cls=None):

        encoding = encoding or self.default_encoding
        template_cls = template_cls or self.template_cls

        filename = normpath(filename)
        if isabs(filename):
            relative_to = None
            filename = relpath(filename, '/')

        if relative_to is not None:
            if isinstance(relative_to, Template):
                relative_to = relative_to.filename
            search_path = chain([dirname(relative_to)], self.search_path)
        else:
            search_path = self.search_path

        cache_key = (filename, (dirname(relative_to)
                                if relative_to is not None
                                else None))
        cached = cached_mtime = None

        try:
            cached, cached_mtime = self._cache[cache_key]
            if not self.auto_reload:
                return cached
        except KeyError:
            if self._persistent_cache:
                try:
                    cached, cached_mtime = self._persistent_cache[cache_key]
                    if not self.auto_reload:
                        return cached
                except KeyError:
                    pass

        path, mtime, openfile = fs_loader(filename, search_path, encoding)
        if cached and mtime <= cached_mtime:
            return cached

        with openfile() as f:
            template = template_cls(f.read(),
                                    path,
                                    loader=self,
                                    translations_factory=self.translations_factory)
        self._cache[cache_key] = template, mtime
        if self._persistent_cache:
            self._persistent_cache[cache_key] = template, mtime
        return template


def fs_loader(filename,
              searchpath,
              encoding,
              getmtime=os.path.getmtime,
              pjoin=os.path.join):
    filepath = None
    mtime = None
    for p in searchpath:
        filepath = pjoin(p, filename)
        if not filepath.startswith(p):
            continue
        try:
            mtime = getmtime(filepath)
        except OSError:
            continue

        if mtime is not None:
            return filepath, mtime, partial(io.open, filepath, encoding=encoding)
    raise TemplateNotFound(filename)

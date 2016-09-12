# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass

# Patch for basestring to work under Python 3
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


class Path(object):

    """Inspired to Django Two-scoops, handling File Paths in Settings.

        >>> from environ import Path
        >>> root = Path('/home')
        >>> root, root(), root('dev')
        (<Path:/home>, '/home', '/home/dev')
        >>> root == Path('/home')
        True
        >>> root in Path('/'), root not in Path('/other/path')
        (True, True)
        >>> root('dev', 'not_existing_dir', required=True)
        Traceback (most recent call last):
        environ.environ.ImproperlyConfigured: Create required path: /home/not_existing_dir
        >>> public = root.path('public')
        >>> public, public.root, public('styles')
        (<Path:/home/public>, '/home/public', '/home/public/styles')
        >>> assets, scripts = public.path('assets'), public.path('assets', 'scripts')
        >>> assets.root, scripts.root
        ('/home/public/assets', '/home/public/assets/scripts')
        >>> assets + 'styles', str(assets + 'styles'), ~assets
        (<Path:/home/public/assets/styles>, '/home/public/assets/styles', <Path:/home/public>)

    """

    def path(self, *paths, **kwargs):
        """Create new Path based on self.root and provided paths.

        :param paths: List of sub paths
        :param kwargs: required=False
        :rtype: Path
        """
        return self.__class__(self.__root__, *paths, **kwargs)

    def file(self, name, *args, **kwargs):
        """Open a file.

        :param name: Filename appended to self.root
        :param args: passed to open()
        :param kwargs: passed to open()

        :rtype: file
        """
        return open(self(name), *args, **kwargs)

    @property
    def root(self):
        """Current directory for this Path"""
        return self.__root__

    def __init__(self, start='', *paths, **kwargs):

        super(Path, self).__init__()

        if kwargs.get('is_file', False):
            start = os.path.dirname(start)

        self.__root__ = self._absolute_join(start, *paths, **kwargs)

    def __call__(self, *paths, **kwargs):
        """Retrieve the absolute path, with appended paths

        :param paths: List of sub path of self.root
        :param kwargs: required=False
        """
        return self._absolute_join(self.__root__, *paths, **kwargs)

    def __eq__(self, other):
        return self.__root__ == other.__root__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Path(self.__root__, other if not isinstance(other, Path) else other.__root__)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.path('../' * other)
        elif isinstance(other, basestring):
            return Path(self.__root__.rstrip(other))
        raise TypeError(
            "unsupported operand type(s) for -: '{0}' and '{1}'".format(self, type(other)))

    def __invert__(self):
        return self.path('..')

    def __contains__(self, item):
        base_path = self.__root__
        if len(base_path) > 1:
            base_path = os.path.join(base_path, '')
        return item.__root__.startswith(base_path)

    def __repr__(self):
        return "<Path:{0}>".format(self.__root__)

    def __str__(self):
        return self.__root__

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, *args, **kwargs):
        return self.__str__().__getitem__(*args, **kwargs)

    def rfind(self, *args, **kwargs):
        return self.__str__().rfind(*args, **kwargs)

    def find(self, *args, **kwargs):
        return self.__str__().find(*args, **kwargs)

    @staticmethod
    def _absolute_join(base, *paths, **kwargs):
        absolute_path = os.path.abspath(os.path.join(base, *paths))
        if kwargs.get('required', False) and not os.path.exists(absolute_path):
            raise ImproperlyConfigured(
                "Create required path: {0}".format(absolute_path))
        return absolute_path
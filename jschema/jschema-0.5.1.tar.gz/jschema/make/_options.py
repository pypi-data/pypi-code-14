# -*- coding: utf-8 -*-
import os
from jschema.errors import JrsMakeError


class Options(object):

    def __init__(self, options):
        self._options = options
        self._dst_dir = None
        self._ns = None
        self._import_root = None

    def _get_param(self, key):
        if key not in self._options:
            raise JrsMakeError("options['{}'] not exists".format(key))
        return self._options[key]

    @property
    def dst_dir(self):
        if self._dst_dir is None:
            dst_dir = self._dst_dir = self._get_param("dst_dir")
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

        return self._dst_dir

    @property
    def ns(self):
        if self._ns is None:
            self._ns = self._get_param("ns")

        return self._ns

    @property
    def import_root(self):
        if self._import_root is None:
            self._import_root = self._get_param("import_root")

        return self._import_root

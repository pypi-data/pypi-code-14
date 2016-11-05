# -*- coding: utf-8 -*-
import os

class BaseCollection(object):

    def the_rightful(self):
        return getattr(self, self.rightful)

    def the_vicious(self):
        return getattr(self, self.vicious)

    def _read_file(self, name, relative_path):
        this_fpath = os.path.dirname(__file__)
        fpath = os.path.join(relative_path, "{}.data".format(name))
        with open(os.path.join(this_fpath, fpath), 'r') as f:
            return f.read().split(',')

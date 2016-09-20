# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import utool as ut


class Directory(ut.NiceRepr):
    """
    self = Directory('.')
    """
    def __init__(self, dpath=None):
        self.dpath = dpath
        self.fpath_list = None
        self.info = None

    def __nice__(self):
        if self.fpath_list is None:
            return '?'
        else:
            return str(len(self.fpath_list))

    def build(self):
        if self.dpath is not None:
            self.dpath = ut.truepath(self.dpath)
            self.fpath_list = ut.glob(self.dpath, '*', with_files=True, with_dirs=False)
            self.info = ut.ColumnLists({'fpath': self.fpath_list})

    def build2(self):
        self.info['nBytes'] = [ut.get_file_nBytes(fpath) for fpath in self.fpath_list]

    def check_duplicates(self):
        subinfo = self.info.get_multis('nBytes')
        subinfo['uuid'] = [ut.get_file_uuid(fpath) for fpath in ut.ProgIter(subinfo['fpath'])]
        subinfo2 = subinfo.get_multis('uuid')
        subinfo2.print()
        #unique_sizes, groupxs = ut.group_indices(self.fsize_list)
        #multi_groupxs = [xs for xs in groupxs if len(xs) > 0]
        #for paths in ut.apply_grouping(self.fpath_list, multi_groupxs):
        #    pass

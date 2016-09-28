#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pub2 (cc) 2016 Ian Dennis Miller

import os
from os.path import join as opj
from .reader import Reader
from .writer import Writer


class File():
    def __init__(self, pub2_obj, filename):
        self.pub2_obj = pub2_obj
        self.filename = filename
        self.working_dir = self.pub2_obj.working_dir

        self.reader = Reader(self)
        self.writer = Writer(self)

        self.preamble = self.reader.preamble
        self.preamble['checksum'] = self.pub2_obj.get_checksum()

        self.content = self.reader.content
        self.identifier = self.reader.identifier

    def is_stale(self):
        """
        return True if the files in pub are older than the one in _pubs.
        """
        bib_filename = opj(self.working_dir, "pub2/{0}.bib".format(self.identifier))
        pdf_filename = opj(self.working_dir, "pub2/{0}.pdf".format(self.identifier))
        html_filename = opj(self.working_dir, "pub2/{0}.html".format(self.identifier))
        preview_filename = opj(self.working_dir, "pub2/{0}.png".format(self.identifier))
        data_filename = opj(self.working_dir, "_data/pub2.json")

        filenames = [
            html_filename,
            bib_filename,
            pdf_filename,
            data_filename,
            preview_filename
        ]

        source_mtime = os.stat(opj(self.working_dir, self.filename))[8]

        for filename in filenames:
            # if a file does not exist, return True
            if not os.path.isfile(opj(self.working_dir, filename)):
                return True

            # if the modification time of the .bib or .pdf is older, return True
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
            if source_mtime > mtime:
                return True

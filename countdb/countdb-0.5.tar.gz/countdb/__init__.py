#!/usr/bin/env python
from __future__ import division

import json
import os
import sys
from shutil import (rmtree, move)


class CountDB(object):

    @staticmethod
    def open(filename):
        self = CountDB(filename)
        self.load()
        return self

    @staticmethod
    def open_for_counting(filename, clean=True):
        self = CountDB(filename, "count")
        if not clean:
            try:
                self.load()
            except:
                pass
        self.counter += 1
        return self

    @staticmethod
    def open_for_extending(filename, clean=True):
        self = CountDB(filename, "extend")
        if not clean:
            try:
                self.load()
            except:
                pass
        return self

    def __init__(self, filename, mode="readonly"):
        self.filename = filename
        self.data = {}
        self.counter = 0
        self.mode = mode

    def load(self):
        with self._open_file(self.filename) as data_file:
            tmp = json.load(data_file)
            self.data = tmp.get("data", {})
            self.counter = tmp.get("counter", 0)

    def dump(self, format=None, stream=None):
        if not format:
            format = "text"
        if not stream:
            stream = sys.stdout
        getattr(self, "dump_" + format)(stream)

    def dump_text(self, stream):
        for key, count in sorted(self.convert_to_relative().items()):
            stream.write("%s %.3f\n" % (key, count))

    def convert_to_relative(self):
        tmp = self.data.copy()
        for key in tmp:
            tmp[key] = tmp[key] / self.counter
        return tmp

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if self.mode != "readonly":
            self.persist()

    def count(self, key, increment=1):
        if self.mode != "count":
            raise Exception("countdb not opened for count (consider using open_for_counting)")
        self.data[key] = self.data.get(key, 0) + increment

    def extend(self, other):
        if self.mode != "extend":
            raise Exception("countdb not opened for extend (consider using open_for_extending)")
        self.counter += other.counter
        for key, count in other.data.items():
            self.data[key] = self.data.get(key, 0) + count

    def persist(self):
        if self.mode == "readonly":
            raise Exception("countdb not opened for modifications "
                            "(consider using open_for_counting or open_for_extending)")
        makedirs(self.filename)
        with self._open_file(self.filename, "w") as data_file:
            json.dump({"data": self.data, "counter": self.counter}, data_file, indent=4)
            data_file.write("\n")

    def finalize(self, final_filename):
        makedirs(final_filename)
        with self._open_file(final_filename, "w") as final_file:
            json.dump(self.convert_to_relative(), final_file, indent=4)
            final_file.write("\n")

    @staticmethod
    def _open_file(filename, mode="r"):
        return open(filename, mode)


def makedirs(filename):
    dirname = os.path.dirname(filename)
    if not dirname:
        return
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != 17:
            raise


def aggregate(dirname):
    if not os.path.isdir(dirname):
        return
    for subdir in os.listdir(dirname):
        aggregate(os.path.join(dirname, subdir))
    tmp_filename = dirname + ".tmp"
    with CountDB.open_for_extending(tmp_filename) as db:
        for f in os.listdir(dirname):
            sub_db = CountDB.open(os.path.join(dirname, f))
            db.extend(sub_db)
    rmtree(dirname)
    move(tmp_filename, dirname)

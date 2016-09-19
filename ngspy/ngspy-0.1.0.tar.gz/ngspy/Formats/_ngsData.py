#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Functions and classes for handling next generation sequencing data.
:author: Manuel Tuschen
:license: FreeBSD

License
----------
Copyright (c) 2016, Manuel Tuschen
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from miscpy import prepareSaving
from miscpy.DataStructure import hstr


class Data:
    def __init__(self, data_type):
        self._header_char = ['#']

        self._data = None
        self._data_type = data_type
        self._extension = ""

        self._len = 0
        self._keys = []

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        try:
            chrom = hstr(key[0])
            n = key[1]
            return self._data[chrom][n]
        except:
            raise KeyError("Key {k}, not found for BED".format(k=key))

    def __setitem__(self, key, value):
        if not isinstance(value, self._data_type):
            raise ValueError(
                "Value must be of type t!".format(t=self._data_type))
        try:
            if self._data is None:
                self._data = {}
            chrom = hstr(key[0])
            n = key[1]
            self._data[chrom][n] = value
            self._len += 1
        except:
            raise KeyError("Key {k}, not found!".format(k=key))

    def __delitem__(self, key):
        try:
            chrom = hstr(key[0])
            n = key[1]
            del self._data[chrom][n]
            if len(self._data[chrom]) == 0:
                self._keys.remove(chrom)
                del self._data[chrom]
            self._len -= 1
        except:
            raise KeyError("Key {k}, not found!".format(k=key))

    def __iter__(self):
        self.__iter = (0, 0)
        return self

    def __next__(self):
        # see if there is another item for the current chrom
        if self.__iter[1] < len(self._data[self._keys[self.__iter[0]]]) - 1:
            pre_iter = (self.__iter[0], self.__iter[1])
            self.__iter = (self.__iter[0], self.__iter[1] + 1)
            return self._data[self._keys[pre_iter[0]]][pre_iter[1]]
        # see if there is another chrom left
        elif self.__iter[0] < len(self._keys) - 1:
            pre_iter = (self.__iter[0], self.__iter[1])
            self.__iter = (self.__iter[0] + 1, 1)
            return self._data[self._keys[pre_iter[0]]][pre_iter[1]]
        # otherwise we are done
        else:
            raise StopIteration

    def append(self, value):
        if self._data is None:
            self._data = {}
        key = hstr(value.chrom)
        if not isinstance(value, self._data_type):
            raise ValueError(
                "Value must be of type {t}!".format(t=self._data_type))
        if key not in self._data:
            self._keys.append(key)
            self._data[key] = []
        self._data[key].append(value)
        self._len += 1

    def sort(self):
        self._keys = sorted(self._keys)
        for key in self._keys:
            self._data[key] = sorted(self._data[key])

    def write(self, name, path, extension="", validate=True):
        if extension == "":
            extension = self._extension
        fname = prepareSaving(name, path, extension=extension)

        with open(fname, 'w') as file:
            # write data
            for key in self._keys:
                for item in self._data[key]:
                    if validate:
                        if not item.valid:
                            raise ValueError(
                                "Can not write file due to invalid data entry: " + str(
                                    item))
                        file.write(str(item))

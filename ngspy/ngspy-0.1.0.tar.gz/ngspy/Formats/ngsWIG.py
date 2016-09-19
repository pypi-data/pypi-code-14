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

from __future__ import division, absolute_import, unicode_literals, \
    print_function

from miscpy import prepareLoading

from ._ngsData import Data
from .ngsBedGraph import BedGraphEntry


__all__ = ["WIG"]


class WIG(Data):
    """
    A BedGraph object is designed to parse data from an BedGraph file
    or write its data to an BedGraph file. BedGraph supports iterator and
    mutable sequence protocols. Items can be accessed by an tuple key (chr, n),
    i.e. the nth entry of chr.

    Attributes
    ----------

    Methods
    -------
    append(value) :
        Append another BEDentry.
    sort() :
        Sort entries;
    parse(name, path, extension="bedGraph", validate=True) :
        Parse data from path/name.extension and store them in the BED object.
    write(name, path, extension="bedGraph", validate=True) :
        Write data to path/name.extension
    """

    def __init__(self):
        super().__init__(BedGraphEntry)

    def parse(self, name, path, extension="bedGraph", validate=True):
        """
        parse WIG file.
        """

        fname = prepareLoading(name, path, extension=extension)
        with open(fname, 'r') as file:
            splitter = '\t'
            counter = 0
            for line in file:
                counter += 1

                # skip header lines
                if line[0] in self.__header_char:
                    continue

                # parse data
                variable = True
                chrom = None
                start = None
                step = None
                span = 1
                # parse step lines

                if "variableStep" in line:
                    variable = True
                    line = line.lstrip("variableStep")
                    line = line.lstrip()
                    line = line.rstrip()

                    # see if there is a span field
                    split = line.find(splitter)
                    if split == -1:
                        # no span so line should be only chrom field
                        _, _, c = line.partition("=")
                        chrom = c
                    else:
                        tmp = line[0:split]
                        _, _, c = tmp.partition("=")
                        chrom = c
                        line = line[split + 1:]
                        _, _, s = line.partition("=")
                        span = int(s)
                    continue

                if "fixedStep" in line:
                    variable = False
                    line = line.lstrip("fixedStep")
                    line = line.lstrip()
                    line = line.rstrip()
                    # look for the chrom
                    split = line.find(splitter)
                    if split == -1:
                        raise ValueError("No 'chrom' field in WIG file!")
                    else:
                        tmp = line[0:split]
                        _, _, c = tmp.partition("=")
                        chrom = c
                    line = line[split + 1:]
                    line = line.lstrip()
                    # look for start
                    if split == -1:
                        raise ValueError("No 'start' field in WIG file!")
                    else:
                        tmp = line[0:split]
                        _, _, s = tmp.partition("=")
                        start = int(start)
                    line = line[split + 1:]
                    line = line.lstrip()
                    # see if there is a span field
                    split = line.find(splitter)
                    if split == -1:
                        # no span so only step field left
                        _, _, s = line.partition("=")
                        step = int(s)
                    else:
                        tmp = line[0:split]
                        _, _, s = tmp.partition("=")
                        step = int(s)
                        line = line[split + 1:]
                        line = line.lstrip()
                        _, _, s = line.partition("=")
                        span = int(s)
                    continue

                if variable:
                    line = line.lstrip()
                    line = line.rstrip()
                    st, _, sc = line.partition(splitter)
                    entry = BedGraphEntry(chrom, int(st), int(st) + span,
                                          float(sc))
                    if validate:
                        if not entry.valid:
                            raise IOError(
                                "Invalid BedGraph file! Entry in line {c} is {e}".format(
                                    c=counter, e=str(entry)))
                    self.append(entry)
                else:
                    line = line.lstrip()
                    line = line.rstrip()
                    entry = BedGraphEntry(chrom, start, start + span,
                                          float(line))
                    entry = BedGraphEntry(chrom, int(st), int(st) + span,
                                          float(sc))
                    if validate:
                        if not entry.valid:
                            raise IOError(
                                "Invalid BedGraph file! Entry in line {c} is {e}".format(
                                    c=counter, e=str(entry)))
                    self.append(entry)
                    start += step

    def write(self, name, path, extension="", validate=True):
        pass

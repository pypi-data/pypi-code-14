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

from miscpy import prepareLoading, prepareSaving

from ._ngsData import Data
from .ngsBED import BED3Entry


__all__ = ["BedGraphEntry", "BedGraph"]


class BedGraphEntry(BED3Entry):
    """
    BedGraph entry.
    https://genome.ucsc.edu/FAQ/FAQformat.html#format1

    Notes on comparing GFF entries.
    Entries are considered equal only if all entries are equal.
    One entry is regarded as larger only if the sequence id is larger or equal
    and the start position is truly larger. One entry is regarded as
    larger-equal only if the sequence id is larger or equal and the start
    position is larger or equal. The same rules apply for smaller.

    Attributes
    ----------
    chrom : basestring
        The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold
        (e.g. scaffold10671)
    chromStart : int
        The starting position of the feature in the chromosome or scaffold. The
        first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold.
        The chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    score : float
        A score between 0 and 1000. If the track line useScore attribute is set
        to 1 for this annotation data set, the score value will determine the
        level of gray in which this feature is displayed (higher numbers =
         darker gray).
    valid : bool
        To check if the entry is a valid one.

    Methods
    -------
    """

    def __init__(self, chrom, chromStart, chromEnd, score):
        super().__init__(chrom, chromStart, chromEnd)
        self.score = score

    def __str__(self):
        sep = self._sep
        newline = self._newline
        score = str(self.score)

        return super().__str__().rstrip() + sep + score + newline

    def __eq__(self, other):

        if super().__eq__(other) and self.score == other.score:
            return True
        else:
            return False

    def _valid(self):

        if not super()._valid():
            return False
        # check score
        if not isinstance(self.score, float):
            return False

        return True


class BedGraph(Data):
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
        self._extension = "bedGraph"

    def parse(self, name, path, extension="bedGraph", validate=True):
        """
        parse BedGraph file.
        """

        fname = prepareLoading(name, path, extension=extension)
        with open(fname, 'r') as file:
            splitter = '\t'
            counter = 0
            for line in file:
                counter += 1

                # skip header lines
                if line[0] in self._header_char:
                    continue

                # parse data
                # find chrom
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BedGraph file! No 'chrom' entry in line {c}".format(
                            c=counter))
                chrom = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find start
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BedGraph file! No 'chromStart' entry in line {c}".format(
                            c=counter))
                chromStart = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find end
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BedGraph file! No 'chromEnd' entry in line {c}".format(
                            c=counter))
                chromEnd = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find score
                line = line.rstrip()
                score = float(line)

                entry = BedGraphEntry(chrom, chromStart, chromEnd, score)
                if validate:
                    if not entry.valid:
                        raise IOError(
                            "Invalid BedGraph file! Entry in line {c} is {e}".format(
                                c=counter, e=str(entry)))
                self.append(entry)
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

from __future__ import division, absolute_import, unicode_literals, \
    print_function
import re

from miscpy import prepareLoading, prepareSaving

from ._ngsData import Data


__all__ = ["BEDEntry", "BED"]


class BED3Entry:
    """
    BED 3 format provides the basic underlying format for the UCSC genome
    browser: https://genome.ucsc.edu/FAQ/FAQformat.html#format1
    It is called BED 3 because it provides 3 entries which are mandatory and
    must be present in all .bed files. Apart from BED 3 there exists several
    derived formats which add additional entries.

 Attributes
    ----------
    chrom : basestring
        The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold
        (e.g. scaffold10671)
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    """

    def __init__(self, chrom, chromStart, chromEnd):
        self._sep = "\t"
        self._newline = "\n"
        self.chrom = chrom
        self.chromStart = chromStart
        self.chromEnd = chromEnd

    def __getattr__(self, valid):
        return self._valid()

    def __str__(self):
        sep = self._sep
        newline = self._newline

        chrom = str(self.chrom)
        chromStart = str(self.chromStart)
        chromEnd = str(self.chromEnd)
        return chrom + sep + chromStart + sep + chromEnd + newline

    def __lt__(self, other):
        """
        One BED 3 is regarded larger only if the chromosome is larger or equal
        and the start position is truly larger.
        """
        if self.chrom <= other.chrom and self.chromStart < other.chromStart:
            return True
        else:
            return False

    def __le__(self, other):
        return not other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        """
        We consider equality only if all entries are equal.
        """
        if self.chrom == other.chrom and self.chromStart == other.chromStart and self.chromEnd == other.chromEnd:
            return True
        else:
            return False

    def __neg__(self, other):
        return not self == other

    def _valid(self):
        pattern = re.compile(".")  # we can have an arbitrary string
        # check chrom
        if not pattern.match(self.chrom):
            return False
        # check start
        if not isinstance(self.chromStart, int):
            return False
        if self.chromStart < 0:
            return False
        # check end
        if not isinstance(self.chromEnd, int):
            return False
        if self.chromEnd <= self.chromStart:
            return False
        return True


class BED6Entry(BED3Entry):
    """
    BED 6 format provides some extensions to the BED 3 formatt:
    https://genome.ucsc.edu/FAQ/FAQformat.html#format1
    It is called BED 6 because it provides 3 more fields compared to BED 3.

 Attributes
    ----------
    chrom : basestring
        The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold
        (e.g. scaffold10671)
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    name : basestring, optional
        Defines the name of the BED line. This label is displayed to the left
        of the BED line in the Genome Browser window when the track is open to
        full display mode or directly to the left of the item in pack mode.
    score : float, optional
        A score between 0 and 1000. If the track line useScore attribute is set
        to 1 for this annotation data set, the score value will determine the
        level of gray in which this feature is displayed (higher numbers =
         darker gray).
    strand : char, optional
        Defines the strand - either '+' or '-'.
    """

    def __init__(self, chrom, chromStart, chromEnd, score, name=None,
                 strand=None):

        super().__init__(chrom, chromStart, chromEnd)
        self.score = score
        self.name = name
        self.strand = strand

    def __str__(self):
        sep = self._sep
        newline = self._newline

        score = str(self.chrom)
        if self.name is None:
            name = "."
        else:
            name = str(self.name)
        if self.strand is None:
            strand = "."
        else:
            stand = str(self.strand)
        return super().__str__().lstrip() + sep + name + sep + score + sep + strand + newline

    def __eq__(self, other):
        """
        We consider equality only if all entries are equal.
        """
        if super().__eq__(
                other) and self.name == other.name and self.score == other.score and self.strand == other.strand:
            return True
        else:
            return False

    def _valid(self):
        pattern = re.compile(".")  # we can have an arbitrary string
        pattern_strand = re.compile("[+-.]")

        if not super().__valid():
            return False

        # check name
        if not (self.name is None or pattern.match(self.name)):
            return False
        # check score
        if not isinstance(self.signalValue, int):
            return False
        # check strand
        if not (self.strand is None or pattern_strand.match(self.strand)):
            return False
        return True


class BEDEntry(BED3Entry):
    """
    Arbritary BED format as specified in :
    https://genome.ucsc.edu/FAQ/FAQformat.html#format1

    Attributes
    ----------
    chrom : basestring
        The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold
        (e.g. scaffold10671)
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    name : basestring, optional
        Defines the name of the BED line. This label is displayed to the left
        of the BED line in the Genome Browser window when the track is open to
        full display mode or directly to the left of the item in pack mode.
    score : float, optional
        A score between 0 and 1000. If the track line useScore attribute is set
        to 1 for this annotation data set, the score value will determine the
        level of gray in which this feature is displayed (higher numbers =
         darker gray).
    strand : char, optional
        Defines the strand - either '+' or '-'.
    thickStart : int, optional
        The starting position at which the feature is drawn thickly (for
        example, the start codon in gene displays). When there is no thick part,
        thickStart and thickEnd are usually set to the chromStart position.
    thickEnd : int, optional
        The ending position at which the feature is drawn thickly (for example,
        the stop codon in gene displays).
    itemRgb : tuble, optional
        An RGB value of the form R,G,B (e.g. 255,0,0). If the track line
        itemRgb attribute is set to "On", this RBG value will determine the
        display color of the data contained in this BED line. NOTE: It is
        recommended that a simple color scheme (eight colors or less) be used
        with this attribute to avoid overwhelming the color resources of the
        Genome Browser and your Internet browser.
    blockCount : int
        The number of blocks (exons) in the BED line.
    blockSizes : list
        A comma-separated list of the block sizes. The number of items in this
        list should correspond to blockCount.
    blockStarts : list
        A comma-separated list of block starts. All of the blockStart positions
        should be calculated relative to chromStart. The number of items in
        this list should correspond to blockCount.
    valid : bool
        To check if the entry is a valid one.

    Methods
    -------
    """

    def __init__(self, chrom, chromStart, chromEnd, name=None, score=None,
                 strand=None, thickStart=None, thickEnd=None, itemRbg=None,
                 blockCount=None, blockSize=None, blockStarts=None):
        super().__init__(chrom, chromStart, chromEnd)
        self.name = name
        self.score = score
        self.strand = strand
        self.thickStart = thickStart
        self.thickEnd = thickEnd
        self.itemRgb = itemRbg
        self.blockCount = blockCount
        self.blockSizes = blockSize
        self.blockStarts = blockStarts

    def __str__(self):
        sep = self._sep
        gsep = ','
        newline = self._newline

        if self.name is None:
            name = ""
        else:
            name = str(self.name)
        if self.score is None:
            score = ""
        else:
            score = str(self.score)
        if self.strand is None:
            strand = ""
        else:
            strand = str(self.strand)
        if self.thickStart is None:
            thickStart = ""
        else:
            thickStart = str(self.thickStart)
        if self.thickEnd is None:
            thickEnd = ""
        else:
            thickEnd = str(self.thickEnd)
        if self.itemRgb is None:
            itemRgb = ""
        else:
            itemRgb = ""
            for item in self.itemRgb:
                itemRgb + str(item) + gsep
            itemRgb = itemRgb.rstrip(gsep)
        if self.blockCount is None:
            blockCount = ""
        else:
            blockCount = str(self.blockCount)
        if self.blockSizes is None:
            blockSizes = ""
        else:
            blockSizes = ""
            for item in self.blockSizes:
                blockSizes + str(item) + gsep
            blockSizes = blockSizes.rstrip(gsep)
        if self.blockStarts is None:
            blockStarts = ""
        else:
            blockStarts = ""
            for item in self.blockStarts:
                blockStarts + str(item) + gsep
            blockStarts = blockStarts.rstrip(gsep)

        val = super().__str__().rstrip() + sep + name + sep + score + sep + strand + sep + thickStart + sep + thickEnd + sep + itemRgb + sep + blockCount + sep + blockSizes + sep + blockStarts
        val = val.rstrip()
        return val + newline

    def __eq__(self, other):

        if super().__eq__(
                other) and self.name == other.naem and self.score == other.score and self.strand == other.strand and self.thickStart == other.thickStart and self.thickEnd == other.thickEnd and self.itemRgb == other.itemRgb and self.blockCount == other.blockCount and self.blockSizes == other.blochSizes and self.blockStarts == other.blockStarts:
            return True
        else:
            return False

    def _valid(self):
        pattern = re.compile(".")
        strand_pattern = re.compile("[+-]]")

        if not super()._valid():
            return False

        # check name:
        if self.name is not None:
            if not pattern.match(self.name):
                return False
        else:
            if not (
                                            self.score is None and self.strand is None and self.thickStart is None and self.thickEnd is None and self.itemRgb is None and self.blockCount is None and self.blockSizes is None and self.blockStarts is None):
                return False

        # check score
        if self.score is not None:
            if not isinstance(self.score, float):
                return False
        else:
            if not (
                                        self.strand is None and self.thickStart is None and self.thickEnd is None and self.itemRgb is None and self.blockCount is None and self.blockSizes is None and self.blockStarts is None):
                return False

        # check strand
        if self.strand is not None:
            if not strand_pattern.match(self.strand):
                return False
        else:
            if not (
                                    self.thickStart is None and self.thickEnd is None and self.itemRgb is None and self.blockCount is None and self.blockSizes is None and self.blockStarts is None):
                return False

        # check thickStart:
        if self.thickStart is not None:
            if not isinstance(self.thickStart, int):
                return False
        else:
            if not (
                                self.thickEnd is None and self.itemRgb is None and self.blockCount is None and self.blockSizes is None and self.blockStarts is None):
                return False

        # check thickEnd:
        if self.thickEnd is not None:
            if not isinstance(self.thickEnd, int):
                return False
        else:
            if not (
                            self.itemRgb is None and self.blockCount is None and self.blockSizes is None and self.blockStarts is None):
                return False

        # check itemRgb:
        if self.itemRgb is not None:
            for item in self.itemRgb:
                if item < 0 or item > 255 and not isinstance(item, int):
                    return False
        else:
            if not (
                        self.blockCount is None and self.blockSizes is None and self.blockStarts is None):
                return False

        # check blockCount:
        if self.blockCount is not None:
            if self.blockSizes is None or self.blockStarts is None:
                return False
            if not isinstance(self.blockCount, int):
                return False
        else:
            if not (self.blockSizes is None and self.blockStarts is None):
                return False

        # check blockSizes:
        if self.blockSizes is not None:
            if len(self.blockSizes) != self.blockCount:
                return False
            for item in self.blockSizes:
                if item < 0 and not isinstance(item, int):
                    return False
        else:
            if not (self.blockSizes is None and self.blockStarts is None):
                return False

        # check blockStarts:
        if self.blockStarts is not None:
            if len(self.blockStarts) != self.blockCount:
                return False
            if self.blockStarts[0] != 0:
                return False
            if self.blockSizes[-1] + self.blockStarts[-1] != self.chromEnd:
                return False
            for item in self.blockStarts:
                if item < 0 and not isinstance(item, int):
                    return False
        return True


class BED(Data):
    """
    A BED object is designed to parse data from an BED file or write its
    data to an BED file. BED supports iterator and mutable sequence protocols.
    Items can be accessed by an tuple key (chr, n), i.e. the nth entry of chr.

    Attributes
    ----------

    Methods
    -------
    append(value) :
        Append another BEDEntry.
    sort() :
        Sort entries;
    parse(name, path, extension="bed", validate=True) :
        Parse data from path/name.extension and store them in the BED object.
    write(name, path, extension="bed", validate=True) :
        Write data to path/name.extension
    """

    def __init__(self):
        super().__init__(BEDEntry)
        self._extension = "bed"

    def parse(self, name, path, extension="bed", validate=True):
        """
        parse BED file.
        """
        fname = prepareLoading(name, path, extension=extension)

        splitter = '\t'
        counter = 0
        with open(fname, 'r') as file:
            self._data = {}

            for line in file:
                counter += 1
                # handel header files
                if line[0] in self._header_char:
                    continue

                # find chrom
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BED file! No 'chrom' entry in line {c}".format(
                            c=counter))
                chrom = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find chromStart
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BED file! No 'chromStart' entry in line {c}".format(
                            c=counter))
                chromStart = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find chromEnd
                split = line.find(splitter)
                if split == -1:
                    chromEnd = int(line[0:])
                else:
                    chromEnd = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                entry = BEDEntry(chrom, chromStart, chromEnd)
                # look for optional fields:

                if len(line) > 0:
                    # find name
                    split = line.find(splitter)
                    if split == -1:
                        entry.name = line[0:]
                    else:
                        entry.name = line[0:split]
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find score
                    split = line.find(splitter)
                    if split == -1:
                        entry.score = float(line[0:])
                    else:
                        entry.score = float(line[0:split])
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find strand
                    split = line.find(splitter)
                    if split == -1:
                        entry.strand = line[0:split]
                    else:
                        entry.strand = line[0:split]
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find thickStart
                    split = line.find(splitter)
                    if split == -1:
                        entry.thickStart = int(line[0:])
                    else:
                        entry.thickStart = int(line[0:split])
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find thickEnd
                    split = line.find(splitter)
                    if split == -1:
                        entry.thickEnd = int(line[0:])
                    else:
                        entry.thickEnd = int(line[0:split])
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find itemRgb
                    entry.itemRgb = []
                    split = line.find(splitter)
                    if split == -1:
                        value = line[0:]
                    else:
                        value = line[0:split]
                    while len(value) > 0:
                        sep = value.find(',')
                        if sep == -1:
                            entry.itemRgb.append(int(value[0:]))
                            break
                        else:
                            entry.itemRgb.append(int(value[0:sep]))
                        value = value[sep + 1:]
                        value = value.lstrip()

                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find blockCount
                    split = line.find(splitter)
                    if split == -1:
                        entry.blockCount = int(line[0:])
                    else:
                        entry.blockCount = int(line[0:split])
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find blockSizes
                    entry.blockSizes = []
                    split = line.find(splitter)
                    if split == -1:
                        value = line[0:]
                    else:
                        value = line[0:split]

                    while len(value) > 0:
                        sep = value.find(',')
                        if sep == -1:
                            entry.blockSizes.append(int(value[0:]))
                            break
                        else:
                            entry.blockSizes.append(int(value[0:sep]))
                        value = value[sep + 1:]
                        value = value.lstrip()
                    line = line[split + 1:]
                    line = line.lstrip()

                if len(line) > 0:
                    # find blockStarts
                    entry.blockStarts = []
                    split = line.find(splitter)
                    if split == -1:
                        value = line[0:]
                    else:
                        value = line[0:split]
                    while len(value) > 0:
                        sep = value.find(',')
                        if sep == -1:
                            entry.blockStarts.append(int(value[0:]))
                            break
                        else:
                            entry.blockStarts.append(int(value[0:sep]))
                        value = value[sep + 1:]
                        value = value.lstrip()

                if validate:
                    if not entry.valid:
                        raise IOError(
                            "Invalid BED file! Entry in line {c} is {e}".format(
                                c=counter, e=str(entry)))

                self.append(entry)


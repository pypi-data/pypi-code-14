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


from __future__ import division, absolute_import, unicode_literals, print_function
import re

from miscpy import prepareLoading

from ._ngsData import Data
from .ngsBED import BED6Entry


__all__ = ["BroadPeakEntry", "NarrowPeakEntry", "BroadPeak", "NarrowPeak"]


class BroadPeakEntry(BED6Entry):
    """
    This format is used to provide called regions of signal enrichment based on
    pooled, normalized (interpreted) data. It is a BED 6+3 format:
    https://genome.ucsc.edu/FAQ/FAQformat.html#format13

 Attributes
    ----------
    chrom : basestring
        Name of the chromosome (or contig, scaffold, etc.).
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    name : basestring
        Name given to a region (preferably unique). Use '.' if no name is
        assigned.
    score : int
        Indicates how dark the peak will be displayed in the browser (0-1000)
    strand : char
         +/- to denote strand or orientation (whenever applicable). Use '.' if
         no orientation is assigned.
    signalValue: float
        Measurement of overall (usually, average) enrichment for the region.
    pValue : float
        Measurement of statistical significance (-log10). Use -1 if no pValue
        is assigned.
    qValue : float
        Measurement of statistical significance using false discovery rate
        (-log10). Use -1 if no qValue is assigned.
    """

    def __init__(self, chrom, chromStart, chromEnd, score, signalValue,
                 name=None, strand=None, pValue=None, qValue=None):

        super().__init__(chrom, chromStart, chromEnd, score, name, strand)
        self.signalValue = signalValue
        self.pValue = pValue
        self.qValue = qValue

    def __str__(self):
        sep = self._sep
        newline = self._newline

        signalValue = str(self.signalValue)
        if self.pValue is None:
            pValue = str(-1)
        else:
            pValue = str(self.pValue)
        if self.qValue is None:
            qValue = str(-1)
        else:
            qValue = str(self.qValue)
        return super().__str__().rstrip() + sep + signalValue + sep + pValue + sep + qValue + newline

    def __eq__(self, other):

        if super().__eq__(
                other) and self.signalValue == other.signalValue and self.pValue == other.pValue and self.qValue == other.qValue:
            return True
        else:
            return False

    def _valid(self):

        if not super()._valid():
            return False

        # check signal Value
        if not isinstance(self.signalValue, float):
            return False
        # check pValue
        if not (self.pValue is None or isinstance(self.pValue,
                                                  float) or self.pValue == -1):
            return False
        # check qValue
        if not (self.qValue is None or isinstance(self.qValue,
                                                  float) or self.qValue == -1):
            return False
        return True


class NarrowPeakEntry(BroadPeakEntry):
    """
    This format is used to provide called regions of signal enrichment based on
    pooled, normalized (interpreted) data. It is a BED 6+3 format:
    https://genome.ucsc.edu/FAQ/FAQformat.html#format12

 Attributes
    ----------
    chrom : basestring
        Name of the chromosome (or contig, scaffold, etc.).
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    name : basestring
        Name given to a region (preferably unique). Use '.' if no name is
        assigned.
    score : int
        Indicates how dark the peak will be displayed in the browser (0-1000)
    strand : char
         +/- to denote strand or orientation (whenever applicable). Use '.' if
         no orientation is assigned.
    signalValue: float
        Measurement of overall (usually, average) enrichment for the region.
    pValue : float
        Measurement of statistical significance (-log10). Use -1 if no pValue
        is assigned.
    qValue : float
        Measurement of statistical significance using false discovery rate
        (-log10). Use -1 if no qValue is assigned.
    peak : int
        Point-source called for this peak; 0-based offset from chromStart. Use -1 if no point-source called
    """

    def __init__(self, chrom, chromStart, chromEnd, score, signalValue,
                 name=None, strand=None, pValue=None, qValue=None, peak=None):

        super().__init__(chrom, chromStart, chromEnd, score, signalValue, name,
                         strand, pValue, qValue)
        self.peak = peak

    def __str__(self):
        sep = self._sep
        newline = self._newline

        if self.peak is None:
            peak = str(-1)
        else:
            peak = str(self.peak)

        return super().__str__().rstrip() + sep + peak + newline

    def __eq__(self, other):

        if super().__eq__(other) and self.peak == other.peak:
            return True
        else:
            return False

    def _valid(self):
        if not super()._valid():
            return False
        # check peak Value
        if not (self.qValue is None or isinstance(self.qValue,
                                                  int) or self.qValue == -1):
            return False
        return True


class RNAelementsEntry(BED6Entry):
    """
    This fromat provides fields for RNAseq data. It is a BED 6+3 format:
    https://genome.ucsc.edu/FAQ/FAQformat.html#format11

 Attributes
    ----------
    chrom : basestring
        Name of the chromosome (or contig, scaffold, etc.).
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    name : basestring
        Name given to a region (preferably unique). Use '.' if no name is
        assigned.
    score : int
        Indicates how dark the peak will be displayed in the browser (0-1000)
    strand : char
         +/- to denote strand or orientation (whenever applicable). Use '.' if
         no orientation is assigned.
    level: float
        Expression level such as RPKM or FPKM.
    signf : float
        Statistical significance such as IDR.
    score2 : float
        Additional measurement/count e.g. number of reads.
    """

    def __init__(self, chrom, chromStart, chromEnd, score, level, signif, score2,
                 name=None, strand=None):
        super().__init__(chrom, chromStart, chromEnd, score, name, strand)
        self.level = level
        self.sifnif = signif
        self.score2 = score2

    def __str__(self):
        sep = self._sep
        newline = self._newline

        level = str(self.level)
        signif = str(self.signif)
        score2 = str(self.score2)

        return super().__str__().rstrip() + sep + level + sep + signif + sep + score2 + newline

    def __eq__(self, other):
        if super().__eq__(other) and self.level == other.level and self.sifnif == other.signif and self.score == other.score:
            return True
        else:
            return False

    def _valid(self):
        if not super().__valid():
            return False

        # check level
        if not isinstance(self.level, float):
            return False
        # check signif
        if not isinstance(self.signif, float):
            return False
        # check score2
        if not isinstance(self.score2, float):
            return False

        return True


class longRNAexpressionEntry(BED6Entry):
    """
    This fromqat provides fields for RNAseq data. It is a BED 6+4 format:
    https://genome.ucsc.edu/FAQ/FAQformat.html#format11

 Attributes
    ----------
    chrom : basestring
        Name of the chromosome (or contig, scaffold, etc.).
    chromStart : int
       The starting position of the feature in the chromosome or scaffold. The
       first base in a chromosome is numbered 0.
    chromEnd : int
        The ending position of the feature in the chromosome or scaffold. The
        chromEnd base is not included in the display of the feature. For
        example, the first 100 bases of a chromosome are defined as
        chromStart=0, chromEnd=100, and span the bases numbered 0-99.
    name : basestring
        Name given to a region (preferably unique). Use '.' if no name is
        assigned.
    score : int
        Indicates how dark the peak will be displayed in the browser (0-1000)
    strand : char
         +/- to denote strand or orientation (whenever applicable). Use '.' if
         no orientation is assigned.
    length: int
        Length of the transcript
    gene_id : basestring
        Gene ID like Ensembl
    coverage : float
        Coverage
    FPKM : float
        FPKM value
    """

    def __init__(self, chrom, chromStart, chromEnd, score, length, gene_id,
                 coverage, fpkm, name=None, strand=None):
        super().__init__(chrom, chromStart, chromEnd, score, name, strand)
        self.length = length
        self.gene_id = gene_id
        self.coverage = coverage
        self.fpkm = fpkm

    def __str__(self):
        sep = self._sep
        newline = self._newline

        length = str(self.length)
        gene_id = str(self.gene_id)
        coverage = str(self.coverage)
        fpkm = str(self.fpkm)

        return super().__str__().rstrip() + sep + length + sep + gene_id + sep + coverage + sep + fpkm + newline

    def __eq__(self, other):
        if super().__eq__(
                other) and self.length == other.length and self.gene_id == other.gene_id and self.coverage == other.coverage and self.fpkm == other.fpkm:
            return True
        else:
            return False

    def _valid(self):
        pattern = re.compile(".")  # we can have an arbitrary string

        if not super()._valid():
            return False

        # check length
        if not isinstance(self.length, int):
            return False
        # check gene_id
        if not isinstance(self.signif, float):
            return False
        # check score2
        if not isinstance(self.score2, float):
            return False

        return True


class ngsBroadPeak(Data):
    """
    A BroadPeak object is designed to parse data from an BroadPeak file or
    write its data to an BroadPeak file. BroadPeak supports iterator and
    mutable sequence protocols. Items can be accessed by an tuple key (chr, n),
    i.e. the nth entry of chr.

    Attributes
    ----------

    Methods
    -------
    append(value) :
        Append another BroadPeakEntry.
    sort() :
        Sort entries;
    parse(name, path, extension="broadPeak", validate=True) :
        Parse data from path/name.extension and store them in the BroadPeak
        object.
    write(name, path, extension="broadPeak", validate=True) :
        Write data to path/name.extension
    """

    def __init__(self):
        super().__init__(BroadPeakEntry)
        self._extension = "broadPeak"

    def parse(self, name, path, extension="broadPeak", validate=True):
        """
        parse BroadPeak file.
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
                        "Invalid BroadPeak file! No 'chrom' entry in line {c}".format(
                            c=counter))
                chrom = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find chromStart
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'chromStart' entry in line {c}".format(
                            c=counter))
                chromStart = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find chromEnd
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'chromEnd' entry in line {c}".format(
                            c=counter))
                else:
                    chromEnd = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find name
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'name' entry in line {c}".format(
                            c=counter))
                else:
                    name = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find score
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'score' entry in line {c}".format(
                            c=counter))
                else:
                    score = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find strand
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'strand' entry in line {c}".format(
                            c=counter))
                else:
                    strand = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find signal value
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'signalValue' entry in line {c}".format(
                            c=counter))
                else:
                    signalValue = float(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find  p value
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid BroadPeak file! No 'pValue' entry in line {c}".format(
                            c=counter))
                else:
                    pValue = float(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find  q value
                split = line.find(splitter)
                if split != -1:
                    raise IOError(
                        "Invalid BroadPeak file! 'qValue' entry should be the last entry in line {c}".format(
                            c=counter))
                else:
                    line = line.lstrip()
                    line = line.rstrip()
                    qValue = float(line)

                entry = BroadPeakEntry(chrom, chromStart, chromEnd, score,
                                       signalValue, name, strand, pValue,
                                       qValue)
                if validate:
                    if not entry.valid:
                        raise IOError(
                            "Invalid BroadPeak file! Entry in line {c} is {e}".format(
                                c=counter, e=str(entry)))

                self.append(entry)


class ngsNarrowPeak(Data):
    """
    A NarrowPeak object is designed to parse data from an BroadPeak file or
    write its data to an NarrowPeak file. NarrowPeak supports iterator and
    mutable sequence protocols. Items can be accessed by an tuple key (chr, n),
    i.e. the nth entry of chr.

    Attributes
    ----------

    Methods
    -------
    append(value) :
        Append another NarrowPeakEntry.
    sort() :
        Sort entries;
    parse(name, path, extension="narrowPeak", validate=True) :
        Parse data from path/name.extension and store them in the BroadPeak
        object.
    write(name, path, extension="narrowPeak", validate=True) :
        Write data to path/name.extension
    """

    def __init__(self):
        super().__init__(NarrowPeakEntry)
        self._extension = "narrowPeak"

    def parse(self, name, path, extension="narrowPeak", validate=True):
        """
        parse BroadPeak file.
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
                        "Invalid NarrowPeak file! No 'chrom' entry in line {c}".format(
                            c=counter))
                chrom = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find chromStart
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'chromStart' entry in line {c}".format(
                            c=counter))
                chromStart = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find chromEnd
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'chromEnd' entry in line {c}".format(
                            c=counter))
                else:
                    chromEnd = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find name
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'name' entry in line {c}".format(
                            c=counter))
                else:
                    name = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find score
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'score' entry in line {c}".format(
                            c=counter))
                else:
                    score = int(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find strand
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'strand' entry in line {c}".format(
                            c=counter))
                else:
                    strand = line[0:split]
                line = line[split + 1:]
                line = line.lstrip()

                # find signal value
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'signalValue' entry in line {c}".format(
                            c=counter))
                else:
                    signalValue = float(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find  p value
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'pValue' entry in line {c}".format(
                            c=counter))
                else:
                    pValue = float(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find  q value
                split = line.find(splitter)
                if split == -1:
                    raise IOError(
                        "Invalid NarrowPeak file! No 'qValue' entry in line {c}".format(
                            c=counter))
                else:
                    qValue = float(line[0:split])
                line = line[split + 1:]
                line = line.lstrip()

                # find peak
                split = line.find(splitter)
                if split != -1:
                    raise IOError(
                        "Invalid NarrowPeak file! 'peak' entry should be the last entry in line {c}".format(
                            c=counter))
                else:
                    line = line.lstrip()
                    line = line.rstrip()
                    peak = int(line)

                entry = NarrowPeakEntry(chrom, chromStart, chromEnd, score,
                                        signalValue, name, strand, pValue,
                                        qValue, peak)
                if validate:
                    if not entry.valid:
                        raise IOError(
                            "Invalid NarrowPeak file! Entry in line {c} is {e}".format(
                                c=counter, e=str(entry)))

                self.append(entry)

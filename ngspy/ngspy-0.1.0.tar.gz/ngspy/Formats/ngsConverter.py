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
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS I" AND
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

from .ngsBED import BED, BEDEntry
from .ngsBedGraph import BedGraph, BedGraphEntry




def fromGFF2BED(inGFF):
    """
    Convert data from GFF to BED. As both formats are not equivalent only
    partial conversion can be performed. All track specific entries are not
    converted. If the name field should be set, an attribute ID must be
    specified. A score can only be set if a name was given. The same is true for
    the strand.

    Parameters
    ----------
    inGFF : GFF
        The GFF object to convert.

    Return
    ------
    outBED : BED
        The converted BED object.
    """
    outBED = BED()
    for gff in inGFF:
        chrom = gff.seqid
        chromStart = gff.start-1  # gff format is 1 based and end inclusive
        chromEnd = gff.end

        bed = BEDEntry(chrom, chromStart, chromEnd)
        if gff.attribues is not None:
            if "ID" in gff.attributes:
                bed.name = gff.attributes["ID"]
                if gff.score is not None:
                    bed.score = gff.score
                    if gff.strand == '+' or gff.strand == '-':
                        bed.strand = gff.strand
        if not bed.valid:
            raise ValueError("Conversion failed due to invalid BED entry")
        outBED.append(bed)
    return outBED


def fromBED2BedGraph(inBED):
    """
    Convert data from  BED to BedGraph.

    Parameters
    ----------
    inBED : BED
        The BED object to convert.

    Return
    ------
    outBedGraph : BedGraph
        The converted BedGraph object.
    """

    outBedGraph = BedGraph()
    for bed in inBED:
        if bed.score is None:
            raise ValueError("Conversion failed due to missing score in BED entry")
        chrom = bed.chrom
        chromStart = bed.chromStart
        chromEnd = bed.chromEnd
        score = bed.score
        bedgr = BedGraphEntry(chrom, chromStart, chromEnd, score)
        if not bedgr.valid:
            raise ValueError("Conversion failed due to invalid BedGraph entry")
        outBedGraph.append(bedgr)
    return outBedGraph


def fromBedGraph2BED(inBedGraph):
    """
    Convert data from BedGraph to  BED. As in BedGraph there is no name filed
    but is required for the score entry the score will not be converted.

    Parameters
    ----------
    inBedGraph : BedGraph
        The BedGraph object to convert.

    Return
    ------
    outBED : BED
        The converted BED object.
    """

    outBED = BED()
    for bedgr in inBedGraph:
        chrom = bedgr.chrom
        chromStart = bedgr.start
        chromEnd = bedgr.end

        bed = BEDEntry(chrom, chromStart, chromEnd)
        if not bed.valid:
            raise ValueError("Conversion failed due to invalid BED entry")
        outBED.append(bed)
    return outBED


def fromWIG2BedGraph(inWIG):
    """
    Convert data from WIG to BedGraph.

    Parameters
    ----------
    inWIG : WIG
        The WIG object to convert.

    Return
    ------
    outBED : BED
        The converted BED object.
    """

    outBedGraph = BedGraph
    for bedgr in inWIG:
        if not bedgr.valid:
            raise ValueError("Conversion failed due to invalid BedGraph entry")
        outBedGraph.append(bedgr)
    return outBedGraph
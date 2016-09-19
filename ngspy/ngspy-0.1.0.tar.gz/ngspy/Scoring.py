
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


from __future__ import division, absolute_import, unicode_literals, print_function

import numpy as np
import pandas as pd

from miscpy import prepareSaving


def scoreRegion(inGFF, inBedGraph, name, path):
    """
    Score a genomic regions specified in an GFF by averaging over a scores from
    a BedGraph object. Scores are written to a .tsv .

    Parmeters
    ---------
    inGFF : ngsGFF
        The GFF object with genomic regions to score.
    inBedGraph : ngsBedGraph
        The BedGraph object with scores for each region.
    name : basestring
        The filename for the output file.
    path : basestring
        The path to write the  output to.
    """
    if len(inGFF) == 0:
        raise ValueError("GFF does not contain any data!")
    if len(inBedGraph) == 0:
        raise ValueError("BedGraph does not contain any data")

    inGFF.sort()
    inBedGraph.sort()

    chrom = []
    start = []
    end = []
    coverage = []
    sum = []
    mean = []
    mean0 = []
    min = []
    max = []

    header = ["chrom", "start", "end", "coverage", "sum", "mean", "mean0", "min", "max"]
    id = []

    # we need to loop over all gff regions
    for gff in inGFF:
        cover = 0
        mi = np.inf
        ma = -np.inf
        score = 0
        chr = gff.seqid
        gff_start = gff.start - 1 # gff format is 1 based and end inclusive
        # and the we need to loop over all BedGraph regions but only for the
        # correct chrom
        for bedgr in inBedGraph.__data[chr]:

            # lets check if we have coverage at
            # gff:   ==============================
            # bg:  -                                -
            if bedgr.chromEnd <= gff_start:
                continue
            if bedgr.chromStart >= gff.end:
                continue

            # complete coverage if gff fragment is smaller:
            # gff:   ==============================
            # bg:    -        -                   -
            # bg:    ------------------------------

            if bedgr.chromEnd <= gff_start and bedgr.chromEnd <= gff.end:
                coverage += bedgr.chromeEnd - bedgr.chromStart
                score += bedgr.score
                mi = min(mi, bedgr.score)
                ma = max(ma, bedgr.score)
                continue

            # partial coverage at the beginning
            # gff:   ==============================
            # bg:   --
            # bg:   -------------------------------
            # bg:   -------------------------------------
            if bedgr.chromStart < gff_start:
                len = min(gff.end, bedgr.chromEnd) - gff_start
                coverage += len
                score += bedgr.score / (bedgr.chromEnd - bedgr.chromStart) * len
                mi = min(mi, bedgr.score)
                ma = max(ma, bedgr.score)
                continue

            # partial coverage at the end
            # gff:   ==============================
            # bg:                                 --
            # bg:    -------------------------------
            if bedgr.chromEnd > gff.end:
                len = bedgr.chromEnd - max(gff_start, bedgr.chromStart)
                coverage += len
                score += bedgr.score / (bedgr.chromEnd - bedgr.chromStart) * len
                mi = min(mi, bedgr.score)
                ma = max(ma, bedgr.score)
                continue

        chrom.append(chr)
        start.append(gff_start)
        end.append(gff.end)
        id.append(gff.attributes["ID"])
        coverage.append(cover)
        sum.append(score)
        mean.append(score / cover)
        mean0.append(score / (gff.end - gff_start))
        min.append(mi)
        max.append(ma)

    # finally we want to store the data as a csv file
    df = pd.DataFrame([chrom, start, end, coverage, sum, mean, mean0, min, max], columns=id)
    df = df.T
    df.columns = header

    fname = prepareSaving(name, path, extension="tsv")
    df.to_csv(fname, sep="\t")
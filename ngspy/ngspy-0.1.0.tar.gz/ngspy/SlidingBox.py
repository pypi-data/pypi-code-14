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

from .Formats import BED, BEDEntry




def sliding_box(start, stop, size, step=1):
    """
    Find sliding boxes of region

    Parameters:
    -----------
    start: int
        0 based start coordinate of the region.
    stop : int
        0 based stop coordinate of the region, i.e. stop is not part of the
        region anymore;
    size : int
        The size of the box regions
    step : int, optional
        The step size of the sliding box.

    Return
    ------
    regions : list
        List of tuples (start,stop) with the extracted regions.
    """
    # we need to truncate if step is no multiple of stop-start
    if (stop - start) / step != 0:
        overhead = (stop-start) % step

        if overhead % 2 == 0:
            start += overhead // 2
            stop -= overhead // 2
        else:
            start += overhead // 2
            stop -= overhead // 2 + 1
    regions = []
    for i in range(0,(stop - start),step):
        regions.append((i+start, i+start+size))
    return regions


def GFF_sliding_boxes(inGFF, name, path, size, step):
    """
    Read from inGFF file and create sliding boxes for each region.
    Score regions according to the scores in BedGraph file.
    Write all results into GFFout.

    Parameters:
    ----------
    inGFF : GFF
        The GFF file with the original regions. An ID attribute is mandatory.
    name : string
        The name of the output file.
    path : string
        The path of the output file
    size : int
        The size of the box regions
    step : int
        The step size of the sliding box.
    """
    if len(inGFF) == 0:
        raise ValueError("No data in input GFF")
    BEDout = BED()

    # parse through all gene regions
    for gff in inGFF:
        regions = sliding_box(gff.start-1, gff.end, size, step)
        ID = gff.attributes["ID"]
        for i,region in enumerate(regions):
            chrom = gff.seqid
            chromStart = region[0]
            chromEnd = region[1]
            name = "{id}_{i}".format(id=ID, i=i)

            entry = BEDEntry(chrom, chromStart, chromEnd, name=name)
            BEDout.append(entry)
    BEDout.write(name, path)



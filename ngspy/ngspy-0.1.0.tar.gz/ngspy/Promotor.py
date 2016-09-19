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
import datetime

from .Formats import GFF, GFF3Entry




def extractProm(inGFF, name, path, upstram=499, downstream=100, filter={}):
    """
    Extract promotor regions from GFF file as provided by GENCODE:
    http://www.gencodegenes.org

    Genes can be filtered by GFF fields and attributes. Results are stored
    in a new GFF file.

    Parameters
    ---------
    inGFF : GFF
        The GFF object with a filled dataset. The entries describe the gene
        regions. From these regions the promoter is extracted.
    name : basestring
        The filename of the resulting GFF file.
    path : basestring
        The path where to save the results
    upstream : int
        Determines how many genes upstream of the TSS shall regarded as
        promoter. (in front of the gene)
    downstream : int
        Determines how many genes downstream of the TSS shall regarded as
        promoter. (inside the gene)
    filter : dict
        Regions in the GFF are only considerd if they match the filter entries.
        Keys can be any attribute in the GFFEntry. For most tags it is checked
        if the attribute value is in the filter. For "start" it is checked if
        the value is higher than the filter. The same is for score. For "end"
        it is checked if the value is lower than the filter.
    """
    def check_attr(filter_attr, item_attr):
        for key in filter_attr.keys():
            if not item_attr[key] in filter_attr[key]:
                return False
        return True

    if len(inGFF) == 0:
        raise ValueError("No data in input GFF")

    outGFF = GFF()
    outGFF._header_general.append("## Promotors extracted at: " + str(datetime.date.today()) + "\n")

    for gff in inGFF:
        # filter if item shall be extracted

        # shall we filer for seqid
        if "seqid" in filter:
            if not gff.seqid in filter["seqid"]:
                continue
        if "source" in filter:
            if not gff.source in filter["source"]:
                continue
        if "type" in filter:
            if not gff.type in filter["type"]:
                continue
        if "start" in filter:
            if not gff.start > filter["start"]:
                continue
        if "end" in filter:
            if not gff.end < filter["end"]:
                continue
        if "score" in filter:
            if gff.score < filter["score"]:
                continue
        if "strand" in filter:
            if not gff.strand in filter["strand"]:
                continue
        if "phase" in filter:
            if not gff.phase in filter["phase"]:
                continue
        if "attributes" in filter:
            if not check_attr(filter["attributes"], gff.attributes):
                continue

        seqid = gff.seqid
        source = "ROI"
        type = "promotor"
        strand = gff.strand
        attributes = {}
        attributes["ID"] = gff.attributes["ID"]

        # TSS varies from + and - strands
        if gff.strand == '-':
            start = gff.end - downstream
            end = gff.end + upstram
        else: # = is assumed for '.'
            start = gff.start - upstram
            end = gff.start + downstream

        entry = GFF3Entry(seqid, source, type, start, end, strand=strand, attributes=attributes)
        outGFF.append(entry)

    outGFF.sort()
    outGFF.write(name, path)
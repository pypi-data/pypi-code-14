#!/usr/bin/env python
#Last-modified: 18 Feb 2016 01:55:43 PM

#         Module/Scripts Description
# 
# Copyright (c) 2008 Yunfei Wang <Yunfei.Wang1@utdallas.edu>
# 
# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).
# 
# @status:  experimental
# @version: 1.0.0
# @author:  Yunfei Wang
# @contact: yfwang0405@gmail.com

# ------------------------------------
# python modules
# ------------------------------------

import os
import sys


# ------------------------------------
# constants
# ------------------------------------

# ------------------------------------
# Misc functions
# ------------------------------------

def ExcelWriter(f,mode="w"):
    import pandas
    if 'a' in mode:
        from openpyxl import load_workbook
        book = load_workbook(f)
        writer = pandas.ExcelWriter(f, engine='openpyxl') 
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        return writer
    elif 'w' in mode:
        return pandas.ExcelWriter(f)


# ------------------------------------
# Classes
# ------------------------------------

class MicroArray(object):
    def reAnnoProbe(datafile,probefile,tolog=False,reorder=None):
        '''
        GEO Array data analysis.
        Parameters:
            datafile: string
                GSEXXX_series_matrix.txt
            probefile: string
                GPLXXXX.bed
            tolog: bool
                do log2 transformation or not.
            reorder: list or None
                A list of new indices.
        '''
        import numpy
        import pandas
        data = pandas.read_table(datafile,index_col=0,comment='!')
        if tolog:
            data = numpy.log2(data+1)
        else:
            data = data - 0
        if reorder is not None:
            data = data.ix[:,[data.columns[i] for i in reorder]]
        data.dropna(axis=0,how='any',inplace=True)
        # read probes
        probes = pandas.read_table(probefile,index_col=0,header=None)
        probes.columns = ['start','stop','pid','score','strand']
        probes.loc[:,'gid'] = [item.split('_')[0] for item in probes.index]
        probes = probes.ix[:,['pid','gid']]
        probes.drop_duplicates(keep='first')
        # merge data
        data = data.merge(probes,how='inner',left_index=True,right_on='pid')
        data = data.groupby('gid').mean() 
        return data
    reAnnoProbe=staticmethod(reAnnoProbe)

    def selectDiffGenes(data):
        from rngslib import Algorithms
        import numpy
        # differential expression
        de = Algorithms.limma_eBayes(data,[1,0]*6)
        idx = numpy.logical_and(de.pvalue<0.05,de.logFC.abs()>1)
        return idx
    selectDiffGenes=staticmethod(selectDiffGenes)
    

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.exit("Example:"+sys.argv[0]+" file1 file2... ")
    for item in IO.BioReader(sys.argv[1],ftype='bed'):
        print item


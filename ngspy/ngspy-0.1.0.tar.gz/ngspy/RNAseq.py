
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


def selectGenes(df, selection):
    """
    Remove all rows (gene_ids) from a data frame which can not be found in
    selection.

    Parameters
    ---------
    df : DataFrame
        The data frame to work with.
    selection : set
        All ids to keep.

    Return
    ------
    df : DataFrame
        The cleand data frame.
    """
    selection = set(selection)

    for id in df.index:
        if id not in selection:
            df = df.drop(id)
    return df

def removeUnexpr(df):

    # we remove 0 fpkms first

    df = df[df.FPKM != 0]
    df = df[df.TPM != 0]
    return df

def keepHighExpr(df, n):
    df.sort_values(by="FPKM",ascending=0)

    return df.ilic([range(0,n)])

def keepVarExpr(df, n):
    pass

def meanVArExpr():
    pass


def selectBound(df, scores, n):


    bound = []
    unbound = []
    nb = 0
    nu = 0

    # go through all gene ids in the given order
    for id in df.index:
        #create list of box_ids
        box_id = ["{id}_{i}".format(id=id, i=i) for i in range(0,60)]
        box_id = set(box_id)

        # extract scores with box_id
        tmp = scores[box_id]

        # lets see if there is at least one box with a positive score
        tmp = tmp > 0
        if tmp.any(0).any(0):
            bound.append(id)
            nb += 1
        else:
            unbound.append(id)
            nu += 1




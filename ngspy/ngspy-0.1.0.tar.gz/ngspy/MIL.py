import datetime
from copy import deepcopy

import numpy as np
import pandas as pd

from GFF import GFF3entry, GFF


def convertGFFtoMIL(scoreGFFs, labelGFF, name, path):

    mil = milData(name)

    ## we have a list of GFFfiles where we can extract scores from
    ## GFF files are assumed to have the same number of data points


    ## load data if not already done
    for gff in scoreGFFs:
        if gff.data is None:
            gff.parse()
    if labelGFF.data is None:
        labelGFF.parse()

    ## check if all gff files have same number of data points
    N_x = len(labelGFF.data)
    for gff in scoreGFFs:
        if len(gff.data) != N_x:
            raise ValueError("All GFF files need same amount of data")


    ## go through all instances
    for i in range(N_x):
        ## collect scores from all GFF files

        scores = np.zeros((len(scoreGFFs)))
        ID = labelGFF.data[i].attributes["ID"]
        for g, gff in enumerate(scoreGFFs):
            if gff.data[i].attributes["ID"] != ID:
                raise ValueError("ID not equal for GFF files")
            scores[g] = gff.data[i].scores
        label = 0
        if labelGFF.data[i].scores > 0:
            label = 1

        mil.add_x(ID, scores, label)

    mil.del_singleEntires()
    mil.scale()
    mil.save(path)

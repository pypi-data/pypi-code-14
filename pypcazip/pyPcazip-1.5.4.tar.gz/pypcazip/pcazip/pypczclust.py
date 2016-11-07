#!/usr/bin/env python -W ignore
"""
                 *** The command line interface for pyPczclust ***

                       Adapted to use the mapping module.
"""

from __future__ import absolute_import, print_function, division

import logging as log

import numpy as np
from scipy import ndimage

from MDPlus.analysis.pca import Pczfile
from MDPlus.analysis import mapping


def pczclust(args): 
    """
    Performs histogram/watershed based clustering on data from a .pcz
    file.
    """

    if args.verbosity is not None:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    p = Pczfile(args.pczfile)

    projs = p.projs[:args.dims].T

    m = mapping.Map(projs,resolution=args.bins, boundary=1)
    mapping.watershed(m)
    out = [m.cluster_id(id) for id in projs]

    np.savetxt(args.outfile,np.c_[projs,out], fmt=("%8.3f"*args.dims + "%5d"))

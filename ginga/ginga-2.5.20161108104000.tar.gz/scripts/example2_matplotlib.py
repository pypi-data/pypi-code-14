#! /usr/bin/env python
#
# example2_matplotlib.py -- Image a FITS file as a PDF.
#
# Eric Jeschke (eric@naoj.org)
#
#
"""
   $ ./example2_matplotlib.py <fitsfile>
"""
from __future__ import print_function
import sys, os
import logging

from ginga import AstroImage
from ginga.mplw import ImageViewMatplotlib
from ginga import cmap
from ginga.util.six.moves import map, zip

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'

def main(options, args):

    app = QtGui.QApplication(sys.argv)
    app.connect(app, QtCore.SIGNAL('lastWindowClosed()'),
                app, QtCore.SLOT('quit()'))

    logger = logging.getLogger("example1")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(STD_FORMAT)
    stderrHdlr = logging.StreamHandler()
    stderrHdlr.setFormatter(fmt)
    logger.addHandler(stderrHdlr)

    fi = ImageView.ImageViewBase(logger)
    rgbmap = fi.get_rgbmap()
    wd, ht = 800, 600
    fi.set_window_size(wd, ht)
    cm = cmap.get_cmap('rainbow3')
    rgbmap.set_cmap(cm)

    # Load fits file
    filepath = args[0]
    image = AstroImage.AstroImage(logger=logger)
    image.load_file(filepath)

    # Make any adjustments to the image that we want
    fi.set_autocut_params('zscale')
    fi.set_image(image)
    # flip sideways
    #fi.transform(False, False, True)
    fi.transform(False, False, False)
    fi.auto_levels()
    fi.center_image()
    fi.zoom_fit()

    fig = matplotlib.figure.Figure(figsize=(wd, ht))
    ax = fig.add_subplot(111)
    #ax.xaxis.set_visible(False)
    #ax.yaxis.set_visible(False)
    ax.autoscale(True, tight=True)
    #ax.set_xticklabels([])
    #ax.set_yticklabels([])
    #ax.set_xlabel('X values')
    #ax.set_ylabel('Y values')
    #ax.set_title('')
    #ax.grid(True)
    canvas = FigureCanvas(fig)

    #img = plt.figimage(A, 0, 0)
    rgbobj = fi.get_rgb_object()
    coords = map(float, fi.get_datarect())
    # extent= (left, right, bottom, top)
    extent=(coords[0], coords[2], coords[1], coords[3])
    print(extent)

    A = rgbobj.get_array('RGB')
    ax.imshow(A, interpolation="none", origin="upper",
              aspect="equal", vmin=0, vmax=255,
              extent=extent)

    w = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(canvas)
    w.setLayout(layout)

    w.resize(wd, ht)
    app.setActiveWindow(w)
    w.show()

    app.exec_()

if __name__ == '__main__':
    main(None, sys.argv[1:])

# END

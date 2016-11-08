#! /usr/bin/env python
#
# example2.py -- Load a fits file into a Ginga widget with a
#          vispy backend.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
#
"""
   $ ./example2.py [fits file]

A Ginga object rendering to a generic matplotlib Figure.  In short,
this allows you to have all the interactive UI goodness of a Ginga widget
window in a matplotlib figure.  You can interactively flip, rotate, pan, zoom,
set cut levels and color map warp a FITS image.  Furthermore, you can plot
using matplotlib plotting on top of the image and the plots will follow all
the transformations.

See the Ginga quick reference
(http://ginga.readthedocs.io/en/latest/quickref.html)
for a list of the interactive features in the standard ginga widget.

example4 produces a simple matplotlib fits view with a couple of overplots.
This shows how you can use the functionality with straight python/matplotlib
sessions.  Run this by supplying a single FITS file on the command line.
"""
from __future__ import print_function

import sys
import numpy as np

#import vispy
#vispy.use('Qt4Agg')
from vispy.plot import Fig
from vispy import app, scene

from ginga.vispyw.ImageViewPilVispy import CanvasView
#from ginga.vispyw.ImageViewVispy import CanvasView
from ginga.vispyw import VispyHelp
from ginga.misc import log
from ginga.AstroImage import AstroImage
from ginga import cmap

# Set to True to get diagnostic logging output
use_logger = True
logger = log.get_logger('example2', level=10, log_stderr=True)

# create a ginga object, initialize some defaults and
# tell it about the figure
viewer = CanvasView(logger)
viewer.enable_autocuts('on')
viewer.enable_autozoom('on')
viewer.set_autocut_params('zscale')
#viewer.set_color_algorithm('power')
viewer.set_cmap(cmap.get_cmap('rainbow3'))

# enable all interactive ginga features
viewer.get_bindings().enable_all(True)

## canvas = viewer.get_canvas()
## canvas.getDrawClass('normimage')
## print(canvas)

# load an image
if len(sys.argv) < 2:
    print("Please provide a FITS file on the command line")
    sys.exit(1)

image = AstroImage(logger)
image.load_file(sys.argv[1])
viewer.set_image(image)
#viewer.rotate(45)

## img_data = image.get_data()
## cut_lo, cut_hi = viewer.get_cut_levels()
## parent = viewer.view.scene

## # get VisPy equivalent of our colormap
## rgbmap = viewer.get_rgbmap()
## g_cm = rgbmap.get_cmap()
## g_cd = rgbmap.get_dist()
## print(g_cd)
## v_cm = VispyHelp.get_vispy_colormap(g_cm, g_cd)

## image = scene.visuals.Image(img_data, interpolation='nearest',
##                             cmap=v_cm,
##                             clim=(cut_lo, cut_hi),
##                             parent=parent, method='subdivide')

## viewer.get_surface().show()
viewer.get_widget().show()

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()

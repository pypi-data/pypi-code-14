#! /usr/bin/env python
#
# example1_wcsaxes.py -- Load a fits file into a Ginga widget with a
#          matplotlib backend and plot using various world coordinates
#          via the "wcsaxes" package.  You can interactively manipulate
#          the view and the plots all follow.
#
# Eric Jeschke (eric@naoj.org)
#
"""
   $ ./example1_wcsaxes.py sky-0.fits
"""
import sys, os
# just in case you want to use qt
os.environ['QT_API'] = 'pyqt'

import matplotlib
options = ['Qt4Agg', 'GTK', 'GTKAgg', 'MacOSX', 'GTKCairo', 'WXAgg',
           'TkAgg', 'QtAgg', 'FltkAgg', 'WX']
# Force a specific toolkit, if you leave commented matplotlib will choose
# an appropriate one for your system
#matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from astropy.wcs import WCS
from astropy.io import fits
from wcsaxes import WCSAxes

from ginga.mplw.ImageViewCanvasMpl import ImageViewCanvas
from ginga.misc import log
from ginga.AstroImage import AstroImage
from ginga import cmap
# add matplotlib colormaps to ginga's own set
cmap.add_matplotlib_cmaps()

# Set to True to get diagnostic logging output
use_logger = False
logger = log.get_logger(null=not use_logger, log_stderr=True)

# create a regular matplotlib figure
fig = plt.figure()

# create a ginga object, initialize some defaults and
# tell it about the figure
fi = ImageViewCanvas(logger)
fi.enable_autocuts('on')
fi.set_autocut_params('zscale')
#fi.set_cmap(cmap.get_cmap('rainbow3'))
fi.set_figure(fig)

# enable all interactive ginga features
fi.get_bindings().enable_all(True)

hdu = fits.open('2MASS_k.fits')[0]
image = AstroImage(logger)
image.load_hdu(hdu)
fi.set_image(image)

# Read in MSX image in Galactic coordinates
hdu_msx = fits.open('msx.fits')[0]
wcs_msx = WCS(hdu_msx.header)

# plot some example graphics via wcsaxes

# Note adding axis from ginga (mpl backend) object
g_ax = fi.add_axes()
g_ax.hold(True)

ax = WCSAxes(fig, [0, 0, 1, 1], wcs=WCS(hdu.header),
                 transData=g_ax.transData)
ax.patch.set_visible(False)
fig.add_axes(ax, frameon=False)

# Overplot contour
ax.contour(hdu_msx.data, transform=ax.get_transform(wcs_msx),
           colors='orange', levels=[2.5e-5, 5e-5,1.e-4])

ax.set_xlim(0., 720.)
ax.set_ylim(0., 720.)

# if you rotate, flip, zoom or pan the the ginga image the graphics
# stay properly plotted.  See quickref of interactive ginga commands here:
#    http://ginga.readthedocs.org/en/latest/quickref.html
plt.show()

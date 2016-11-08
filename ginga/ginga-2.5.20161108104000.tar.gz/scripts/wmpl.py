from __future__ import print_function
#! /usr/bin/env python
#
# example1.py -- Simple, configurable FITS viewer.
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c) Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import sys, os
import logging
import gtk

from ginga.gtkw.ImageViewGtk import ImageViewZoom
from ginga.gtkw import FileSelection
from ginga.AstroImage import pyfits

import matplotlib
matplotlib.use('GTKCairo')
from  matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo \
     as FigureCanvas

import numpy as np
import matplotlib.pyplot as plt
import random


STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'

class FitsViewer(object):

    def __init__(self, logger):

        self.logger = logger
        root = gtk.Window(gtk.WINDOW_TOPLEVEL)
        root.set_title("ImageViewZoom Example")
        root.set_border_width(2)
        root.connect("delete_event", lambda w, e: self.quit(w))
        self.root = root
        
        self.select = FileSelection.FileSelection()
        vbox = gtk.VBox(spacing=2)

        fi = ImageViewZoom(logger)
        fi.enable_autocuts('on')
        fi.enable_zoom('on')
        fi.enable_cuts(True)
        fi.enable_flip(True)
        fi.enable_rotate(True)
        fi.set_callback('drag-drop', self.drop_file)
        fi.ui_setActive(True)
        self.fitsimage = fi

        w = fi.get_widget()
        w.set_size_request(512, 512)

        vbox.pack_start(w, fill=True, expand=True)

        hbox = gtk.HButtonBox()
        hbox.set_layout(gtk.BUTTONBOX_END)

        wopen = gtk.Button("Open File")
        wopen.connect('clicked', self.open_file)
        wquit = gtk.Button("Quit")
        wquit.connect('clicked', self.quit)

        for w in (wopen, wquit):
            hbox.add(w)

        vbox.pack_start(hbox, fill=False, expand=False)
        root.add(vbox)

    def get_widget(self):
        return self.root

    def load_file(self, filepath):
        in_f = pyfits.open(filepath, 'readonly')
        data = in_f[0].data
        # compressed FITS file?
        if (data == None) and (len(in_f) > 1) and \
           isinstance(in_f[1], pyfits.core.CompImageHDU):
            data = in_f[1].data
        in_f.close()

        self.fitsimage.set_data(data)
        self.root.set_title(filepath)

        fig = plt.figure()
        self.canvas = FigureCanvas(fig)
        self.canvas.set_ctx_from_surface(self.fitsimage.get_surface())
        ax = fig.add_subplot(111)
        N = 30
        x = random.randrange(1, N)
        y = random.randrange(1, N)
        area = np.pi*(10 * random.randrange(1, N))**2 # 0 to 10 point radiuses
        ax.scatter(x,y,s=area, marker='^', c='r')
        line, = ax.plot(np.random.rand(10))
        #ax.set_ylim(0, 1)
        #plt.show()
        self.canvas.show_all()
        print("DONE!")
        
    def open_file(self, w):
        self.select.popup("Open FITS file", self.load_file)

    def drop_file(self, fitsimage, paths):
        fileName = paths[0]
        self.load_file(fileName)
        
    def quit(self, w):
        gtk.main_quit()
        return True

        
def main(options, args):

    logger = logging.getLogger("example1")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(STD_FORMAT)
    stderrHdlr = logging.StreamHandler()
    stderrHdlr.setFormatter(fmt)
    logger.addHandler(stderrHdlr)

    fv = FitsViewer(logger)
    root = fv.get_widget()
    root.show_all()

    if len(args) > 0:
        fv.load_file(fi, args[0])

    gtk.mainloop()

    
if __name__ == '__main__':
    main(None, sys.argv[1:])
    
# END


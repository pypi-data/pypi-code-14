#! /usr/bin/env python
#
# gemini_ql.py -- Simple example of Gemini quicklook
#
# Eric Jeschke (eric@naoj.org)
#
#
from __future__ import print_function
import sys, os
import time
import logging
import math
import numpy

from ginga import AstroImage, RGBImage
from ginga.ImageViewCanvas import Image
from ginga import trcalc
from ginga.qtw.QtHelp import QtGui, QtCore
from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas

import astropy.io.fits as pyfits

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'

class FitsViewer(QtGui.QMainWindow):

    def __init__(self, logger):
        super(FitsViewer, self).__init__()
        self.logger = logger

        maxwd, maxht = 6360, 4616
        self.ovr_rgb = numpy.zeros((maxht, maxwd, 4), dtype=numpy.uint8)
        red = self.ovr_rgb[:, :, 0]
        red[:, :] = 255
        self.rgb_img = RGBImage.RGBImage(data_np=self.ovr_rgb)
        self.alpha = 0.5

        fi = ImageViewCanvas(self.logger, render='widget')
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        fi.set_zoom_algorithm('rate')
        fi.set_zoomrate(1.6)
        fi.set_callback('drag-drop', self.drop_file)
        fi.set_bg(0.2, 0.2, 0.2)
        fi.ui_setActive(True)
        fi.enable_overlays(True)
        self.fitsimage = fi

        bd = fi.get_bindings()
        bd.enable_all(True)

        w = fi.get_widget()
        w.resize(512, 512)

        overlay = Image(0, 0, self.rgb_img)
        self.fitsimage.add(overlay, tag='saturation')

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
        vbox.setSpacing(1)
        vbox.addWidget(w, stretch=1)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))

        wopen = QtGui.QPushButton("Open File")
        wopen.clicked.connect(self.open_file)
        wquit = QtGui.QPushButton("Quit")
        self.connect(wquit,
                     QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))

        hbox.addStretch(1)
        for w in (wopen, wquit):
            hbox.addWidget(w, stretch=0)

        hw = QtGui.QWidget()
        hw.setLayout(hbox)
        vbox.addWidget(hw, stretch=0)

        vw = QtGui.QWidget()
        self.setCentralWidget(vw)
        vw.setLayout(vbox)

    def get_overlay(self, image, saturation):
        data = image.get_data()
        idx = data >= saturation
        # set red channel of RGB overlay according to saturation
        alpha = self.ovr_rgb[:, :, 3]
        alpha[:, :] = 0
        alpha[idx] = int(255 * self.alpha)
        return self.rgb_img
        
    def load_file(self, filepath):
        time_start = time.time()
        image = self.load_gmos(filepath)
        time_elapsed = time.time() - time_start
        print("%.2f sec to create mosaic" % (time_elapsed))
        time_start = time.time()
        rgb_img = self.get_overlay(image, 50000.0)

        time_elapsed = time.time() - time_start
        print("%.2f sec to create overlay" % (time_elapsed))
        
        self.fitsimage.set_image(image, redraw=False)
        self.setWindowTitle(filepath)
        
    def load_gmos(self, filepath):

        dst_arr = numpy.zeros((4616, 6360))
        offsets = [(-1591, 0), (-2582, 1), (498, 2), (-496, 2), (1593, 0),
                   (2583, -1)]
        
        my_ctr_x, my_ctr_y = trcalc.get_center(dst_arr)
        
        with pyfits.open(filepath, 'readonly') as in_f:
            for i in range(6):
                data = in_f[i+1].data
                print(i, data.shape)
                ctr_x, ctr_y = trcalc.get_center(data)
                ht, wd = data.shape
                off_x, off_y = offsets[i]

                x0, y0 = my_ctr_x + off_x, my_ctr_y + off_y
                xlo, xhi = x0 - ctr_x, x0 + wd - ctr_x
                ylo, yhi = y0 - ctr_y, y0 + ht - ctr_y

                dst_arr[ylo:yhi, xlo:xhi, ...] = data[0:ht, 0:wd, ...]

        img_mosaic = AstroImage.AstroImage(logger=self.logger)
        img_mosaic.set_data(dst_arr)
        return img_mosaic


    def open_file(self):
        res = QtGui.QFileDialog.getOpenFileName(self, "Open FITS file",
                                                ".", "FITS files (*.fits)")
        if isinstance(res, tuple):
            fileName = res[0].encode('ascii')
        else:
            fileName = str(res)
        self.load_file(fileName)

    def drop_file(self, fitsimage, paths):
        fileName = paths[0]
        self.load_file(fileName)

        
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

    w = FitsViewer(logger)
    w.resize(524, 540)
    w.show()
    app.setActiveWindow(w)
    w.raise_()
    w.activateWindow()

    if len(args) > 0:
        w.load_file(args[0])

    app.exec_()

if __name__ == '__main__':
    main(None, sys.argv[1:])
    
# END

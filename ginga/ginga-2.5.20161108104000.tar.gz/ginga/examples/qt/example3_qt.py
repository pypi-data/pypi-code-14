#! /usr/bin/env python
#
# example3_qt.py -- Simple, configurable FITS viewer.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from __future__ import print_function
import sys, os
import logging, logging.handlers
from ginga.qtw.QtHelp import QtGui, QtCore

from ginga.util import io_fits
from ginga import AstroImage, RGBImage
from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas
from ginga.canvas.types.image import NormImage, Image
from ginga import colors

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'


class FitsViewer(QtGui.QMainWindow):

    def __init__(self, logger):
        super(FitsViewer, self).__init__()
        self.logger = logger
        self.drawcolors = colors.get_colors()

        fi = ImageViewCanvas(logger, render='widget')
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        fi.enable_draw(True)
        fi.enable_overlays(True)
        fi.set_drawtype('ruler')
        fi.set_drawcolor('blue')
        fi.set_callback('drag-drop', self.drop_file)
        fi.set_callback('none-move', self.motion)
        fi.set_bg(0.2, 0.2, 0.2)
        fi.set_zoom_algorithm('rate')
        fi.set_zoomrate(1.4)
        fi.ui_setActive(True)
        fi.show_pan_mark(True)
        self.view = fi

        bd = fi.get_bindings()
        bd.enable_all(True)
        bm = fi.get_bindmap()
        bm.add_callback('mode-set', self.mode_set_cb)

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
        vbox.setSpacing(1)

        self.mode_w = None
        self.mode_actns = {}
        tb = QtGui.QToolBar()
        agroup = QtGui.QActionGroup(tb)
        agroup.setExclusive(True)
        action = tb.addAction("Pan")
        self.mode_actns['pan'] = action
        action.setCheckable(True)
        action.toggled.connect(lambda tf: self.mode_cb('pan', tf))
        action = agroup.addAction(action)
        action = tb.addAction("Rotate")
        self.mode_actns['rotate'] = action
        action.setCheckable(True)
        action.toggled.connect(lambda tf: self.mode_cb('rotate', tf))
        action = agroup.addAction(action)
        action = tb.addAction("CMap")
        self.mode_actns['cmap'] = action
        action.setCheckable(True)
        action.toggled.connect(lambda tf: self.mode_cb('cmap', tf))
        action = agroup.addAction(action)
        action = tb.addAction("Cuts")
        self.mode_actns['cuts'] = action
        action.setCheckable(True)
        action.toggled.connect(lambda tf: self.mode_cb('cuts', tf))
        action = agroup.addAction(action)
        vbox.addWidget(tb, stretch=0)

        w = fi.get_widget()
        w.resize(512, 512)
        vbox.addWidget(w, stretch=1)

        self.readout = QtGui.QLabel("")
        vbox.addWidget(self.readout, stretch=0,
                       alignment=QtCore.Qt.AlignCenter)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))

        wdrawtype = QtGui.QComboBox()
        self.drawtypes = fi.get_drawtypes()
        for name in self.drawtypes:
            wdrawtype.addItem(name)
        index = self.drawtypes.index('ruler')
        wdrawtype.setCurrentIndex(index)
        wdrawtype.activated.connect(self.set_drawparams)
        self.wdrawtype = wdrawtype

        wdrawcolor = QtGui.QComboBox()
        for name in self.drawcolors:
            wdrawcolor.addItem(name)
        index = self.drawcolors.index('blue')
        wdrawcolor.setCurrentIndex(index)
        wdrawcolor.activated.connect(self.set_drawparams)
        self.wdrawcolor = wdrawcolor

        wclear = QtGui.QPushButton("Clear Canvas")
        wclear.clicked.connect(self.clear_canvas)
        wopen = QtGui.QPushButton("Open File")
        wopen.clicked.connect(self.open_file)
        wquit = QtGui.QPushButton("Quit")
        wquit.clicked.connect(self.quit)

        hbox.addStretch(1)
        for w in (wopen, wdrawtype, wdrawcolor, wclear, wquit):
            hbox.addWidget(w, stretch=0)

        hw = QtGui.QWidget()
        hw.setLayout(hbox)
        vbox.addWidget(hw, stretch=0)

        vw = QtGui.QWidget()
        self.setCentralWidget(vw)
        vw.setLayout(vbox)

    def set_drawparams(self, kind):
        index = self.wdrawtype.currentIndex()
        kind = self.drawtypes[index]
        index = self.wdrawcolor.currentIndex()

        params = { 'color': self.drawcolors[index], }
        self.view.set_drawtype(kind, **params)

    def clear_canvas(self):
        self.view.delete_all_objects()

    def load_file(self, filepath):
        image = AstroImage.AstroImage(logger=self.logger)
        image.load_file(filepath)

        self.view.set_image(image)
        self.setWindowTitle(filepath)

    def open_file(self):
        res = QtGui.QFileDialog.getOpenFileName(self, "Open FITS file",
                                                     ".", "FITS files (*.fits)")
        if isinstance(res, tuple):
            fileName = res[0]
        else:
            fileName = str(res)
        if len(fileName) != 0:
            self.load_file(fileName)

    def drop_file(self, view, paths):
        fileName = paths[0][7:]
        rgbimg = RGBImage.RGBImage()
        rgbimg.load_file(fileName)
        image = Image(-500, -500, rgbimg, alpha=0.3, flipy=True)
        ## rgbimg = AstroImage.AstroImage()
        ## rgbimg.load_file(fileName)
        ## image = NormImage(-500, -500, rgbimg, alpha=0.6)
        #aimage = self.view.get_image()
        #wd, ht = aimage.get_size()
        tag = self.view.add(image)
        ## fileName = paths[0]
        ## self.load_file(fileName)

    def motion(self, view, button, data_x, data_y):

        # Get the value under the data coordinates
        try:
            #value = view.get_data(data_x, data_y)
            # We report the value across the pixel, even though the coords
            # change halfway across the pixel
            value = view.get_data(int(data_x+0.5), int(data_y+0.5))

        except Exception:
            value = None

        fits_x, fits_y = data_x + 1, data_y + 1

        # Calculate WCS RA
        try:
            # NOTE: image function operates on DATA space coords
            image = view.get_image()
            if image is None:
                # No image loaded
                return
            ra_txt, dec_txt = image.pixtoradec(fits_x, fits_y,
                                               format='str', coords='fits')
        except Exception as e:
            self.logger.warning("Bad coordinate conversion: %s" % (
                str(e)))
            ra_txt  = 'BAD WCS'
            dec_txt = 'BAD WCS'

        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (
            ra_txt, dec_txt, fits_x, fits_y, value)
        self.readout.setText(text)

    def quit(self, *args):
        self.logger.info("Attempting to shut down the application...")
        self.deleteLater()

    def mode_cb(self, modname, tf):
        print("%s mode %s" % (modname, tf))
        bm = self.view.get_bindmap()
        if not tf:
            bm.reset_mode(self.view)
            self.mode_w = None
            return
        bm.set_mode(modname, modtype='locked')
        self.mode_w = self.mode_actns[modname]
        return True

    def mode_set_cb(self, bm, mode, mtype):
        print("mode set %s" % (mode))
        if not (mode in self.mode_actns) and self.mode_w:
            self.mode_w.setChecked(False)
            self.mode_w = None
        return True

def main(options, args):

    #QtGui.QApplication.setGraphicsSystem('raster')
    app = QtGui.QApplication(args)

    logger = logging.getLogger("example2")
    logger.setLevel(options.loglevel)
    fmt = logging.Formatter(STD_FORMAT)
    if options.logfile:
        fileHdlr  = logging.handlers.RotatingFileHandler(options.logfile)
        fileHdlr.setLevel(options.loglevel)
        fileHdlr.setFormatter(fmt)
        logger.addHandler(fileHdlr)

    if options.logstderr:
        stderrHdlr = logging.StreamHandler()
        stderrHdlr.setLevel(options.loglevel)
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

if __name__ == "__main__":

    # Parse command line options with nifty optparse module
    from optparse import OptionParser

    usage = "usage: %prog [options] cmd [args]"
    optprs = OptionParser(usage=usage, version=('%%prog'))

    optprs.add_option("--debug", dest="debug", default=False, action="store_true",
                      help="Enter the pdb debugger on main()")
    optprs.add_option("--log", dest="logfile", metavar="FILE",
                      help="Write logging output to FILE")
    optprs.add_option("--loglevel", dest="loglevel", metavar="LEVEL",
                      type='int', default=logging.INFO,
                      help="Set logging level to LEVEL")
    optprs.add_option("--stderr", dest="logstderr", default=False,
                      action="store_true",
                      help="Copy logging also to stderr")
    optprs.add_option("--profile", dest="profile", action="store_true",
                      default=False,
                      help="Run the profiler on main()")

    (options, args) = optprs.parse_args(sys.argv[1:])

    # Are we debugging this?
    if options.debug:
        import pdb

        pdb.run('main(options, args)')

    # Are we profiling this?
    elif options.profile:
        import profile

        print(("%s profile:" % sys.argv[0]))
        profile.run('main(options, args)')


    else:
        main(options, args)

# END

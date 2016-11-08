#! /usr/bin/env python
#
# ss.py -- photo screen saver example with Ginga
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c)  Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
"""
Usage:
    $ ss.py [log options] <directory>
    
"""
from __future__ import print_function
import sys, os
import glob
import time
import logging
import threading
import random
import numpy

from ginga.qtw.QtHelp import QtGui, QtCore
from ginga.qtw import QtMain
from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas
from ginga import RGBImage, BaseImage, LayerImage, AstroImage
from ginga import AutoCuts, RGBMap

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'


class PhotoLayer(LayerImage.LayerImage, RGBImage.RGBImage):

    def __init__(self, logger=None):
        RGBImage.RGBImage.__init__(self, logger=logger)
        LayerImage.LayerImage.__init__(self)

class GingaPhotoShow(QtGui.QMainWindow):

    def __init__(self, qtmain, logger, ev_quit, options):
        super(GingaPhotoShow, self).__init__()
        self.qtmain = qtmain
        self.logger = logger
        self.ev_quit = ev_quit

        # playback rate; changed when we know the actual rate
        self.fps = 30
        #self.playback_rate = 1.0 / self.fps
        self.playback_rate = 7.0
        self.rot_dir = -1

        # Use an AstroImage, not RGBImage for now because we get a
        # different default (faster) scaling algorithm
        self.img_all = PhotoLayer()
        self.img_bg = RGBImage.RGBImage()
        self.img_fg = RGBImage.RGBImage()
        self.img_alpha = BaseImage.BaseImage()
        self.img_all.insert_layer(0, self.img_bg, name="bg", alpha=1.0)
        self.img_all.insert_layer(0, self.img_fg, name="fg", alpha=0.0)

        fi = ImageViewCanvas(self.logger, render='widget')
        fi.enable_autocuts('off')
        fi.set_autocut_params('histogram')
        fi.enable_autozoom('off')
        fi.cut_levels(0, 255)
        fi.set_bg(0.2, 0.2, 0.2)
        # flip y
        fi.transform(False, False, False)
        fi.ui_setActive(True)
        fi.add_callback('configure', self.resize_cb)
        self.canvas = fi

        # Some optomizations to smooth playback at decent FPS
        #fi.set_redraw_lag(self.playback_rate)
        fi.set_redraw_lag(0.0)
        fi._invertY = False
        # PassThruRGBMapper doesn't color map data--data is already colored
        rgbmap = RGBMap.PassThruRGBMapper(self.logger)
        fi.set_rgbmap(rgbmap)
        # Clip cuts assumes data does not need to be scaled in cut levels--
        # only clipped
        fi.set_autocuts(AutoCuts.Clip(logger=self.logger))

        bd = fi.get_bindings()
        bd.enable_pan(True)
        bd.enable_zoom(True)
        bd.enable_cuts(True)
        bd.enable_flip(True)
        bd.enable_cmap(True)

        w = fi.get_widget()
        w.resize(512, 512)

        fi.set_image(self.img_all)
        
        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
        vbox.setSpacing(1)
        vbox.addWidget(w, stretch=1)

        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(QtCore.QMargins(4, 2, 4, 2))

        wopen = QtGui.QPushButton("Open File")
        #wopen.clicked.connect(self.open_file)
        wquit = QtGui.QPushButton("Quit")
        wquit.clicked.connect(self.quit)

        hbox.addStretch(1)
        for w in (wopen, wquit):
            hbox.addWidget(w, stretch=0)

        hw = QtGui.QWidget()
        hw.setLayout(hbox)
        vbox.addWidget(hw, stretch=0)

        vw = QtGui.QWidget()
        self.setCentralWidget(vw)
        vw.setLayout(vbox)

        self.setWindowTitle("Ginga Photo Show")

    def quit(self):
        self.logger.info("quit called")
        self.deleteLater()
        self.ev_quit.set()

    def closeEvent(self, event):
        self.quit()

    def set_playback_rate(self, fps):
        self.fps = fps
        self.playback_rate = 1.0 / self.fps
        self.canvas.set_redraw_lag(self.playback_rate)

    def resize_cb(self, imgview, win_wd, win_ht):
        zeros = numpy.zeros((win_ht, win_wd, 4), dtype=numpy.uint8)
        data = zeros + 70
        data[:, :, 3] = 255   # alpha
        self.img_bg.set_data(data)
        self.img_fg.set_data(zeros)
        alpha = numpy.zeros((win_ht, win_wd))
        self.img_alpha.set_data(alpha)
        self.img_all.set_alpha(0, alpha)
        self.canvas.set_image(self.img_top)
        self.canvas.center_image()
        
    def show_frame(self, img):
        self.logger.debug("updating image")

        start_time = time.time()

        # figure out min(max) of window size
        win_wd, win_ht = self.canvas.get_window_size()
        max_px = min(win_wd, win_ht)

        pic_px = int(1.25 * max_px)
        img_wd, img_ht = img.get_size()
        scale_start = pic_px / float(max(img_wd, img_ht))

        pic_px = int(0.50 * max_px)
        img_wd, img_ht = img.get_size()
        scale_end = pic_px / float(max(img_wd, img_ht))

        loc_x = random.randint(win_wd//4*1, win_wd//4*3)
        loc_y = random.randint(win_ht//4*1, win_ht//4*3)

        alpha_incr = 1 / float(self.fps)
        alpha_base = 0.0
        # reset fg alpha to zero
        alpha = self.img_alpha.get_data()
        alpha[:,:] = alpha_base

        scale_incr = (scale_start - scale_end) / float(self.fps)
        scale_base = scale_start
        
        sleep_time = 0.25
        self.rot_dir *= -1
        
        for i in range(self.fps):
            bnch = img.get_scaled_cutout(0, 0, img_wd, img_ht,
                                         scale_base, scale_base,
                                         method='basic')

            sc_ht, sc_wd, sc_dp = bnch.data.shape[:3]
            if sc_dp <= 3:
                # add alpha channel if there is not one already
                zeros = numpy.zeros((sc_ht, sc_wd, 1), dtype=numpy.uint8)
                zeros += 255
                bnch.data = numpy.append(bnch.data, zeros, 2) 
            img_new = RGBImage.RGBImage(data_np=bnch.data)
            img_new.rotate(self.rot_dir * i)
            sc_wd, sc_ht = img_new.get_size()
            self.logger.debug("cutout size is %dx%d" % (sc_wd, sc_ht))
            sc_data = img_new.get_data()
            if loc_x+sc_wd > win_wd:
                sc_data = sc_data[:,0:win_wd-loc_x]
            if loc_y+sc_ht > win_ht:
                sc_data = sc_data[0:win_ht-loc_y,:]
            sc_ht, sc_wd = sc_data.shape[:2]
            max_sc = max(sc_ht, sc_wd)

            fg_data = self.img_fg.get_data()
            fg_data[:,:] = 0
            fg_data[loc_y:loc_y+sc_ht, loc_x:loc_x+sc_wd] = sc_data
            
            alpha[:,:] = 0
            alpha[loc_y:loc_y+sc_ht, loc_x:loc_x+sc_wd] += alpha_base

            self.img_all.compose_layers()
            self.qtmain.gui_do(self.canvas.redraw)
            time.sleep(sleep_time)
            alpha_base += alpha_incr
            scale_base -= scale_incr

        # merge down
        data = self.img_all.get_data()
        self.img_bg.set_data(data)

        # reset fg to blank
        zeros = numpy.zeros((win_ht, win_wd, 4), dtype=numpy.uint8)
        alpha[:,:] = 0.0
        self.img_fg.set_data(zeros)
        self.img_all.compose_layers()

        self.qtmain.gui_do(self.canvas.redraw)
        

    def photo_show(self, photo_dir):
        
        self.logger.info("photo show loop starting...")

        # get list of photos
        photos = glob.glob(photo_dir + '/*.jpg')
        photos.extend(glob.glob(photo_dir + '/*.jpeg'))
        photos.extend(glob.glob(photo_dir + '/*.JPG'))
        photos.extend(glob.glob(photo_dir + '/*.JPEG'))

        print("photos are:", photos)
        
        while not self.ev_quit.isSet() and len(photos) > 0:
            fn = photos.pop()

            try:
                img = RGBImage.RGBImage(logger=self.logger)
                img.load_file(fn)

                print("showing %s" % (fn))
                self.show_frame(img)

            except Exception as e:
                self.logger.error("error showing image: %s" % str(e))

        self.logger.info("photo show loop terminating...")


def main(options, args):

    # Set up the logger
    logger = logging.getLogger("ss")
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

    # event for synchronizing exit of all threads
    ev_quit = threading.Event()

    # Create top level of Qt application w/custom event loop
    myqt = QtMain.QtMain(logger=logger, ev_quit=ev_quit)

    gv = GingaPhotoShow(myqt, logger, ev_quit, options)
    gv.resize(1024, 900)
    gv.show()

    # start photo show thread
    if len(args) > 0:
        dirname = args[0]
    else:
        dirname = "."
        
    t = threading.Thread(target=gv.photo_show, args=[dirname])
    t.start()

    #app.setActiveWindow(w)
    gv.raise_()
    gv.activateWindow()

    myqt.mainloop()
    logger.info("program terminating...")
    sys.exit(0)

if __name__ == '__main__':
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
    optprs.add_option("--port", dest="port", metavar="NUM",
                      type='int', default=23099,
                      help="Port to use for receiving data")
    optprs.add_option("--other", dest="other", metavar="HOST",
                      help="Host to communicate with")
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

    
#END

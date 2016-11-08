#! /usr/bin/env python
#
# gingavision.py -- video capture example with Ginga
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c)  Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from __future__ import print_function
import sys, os
import time
import logging
import threading
import Queue
import numpy

from ginga.qtw.QtHelp import QtGui, QtCore
from ginga.qtw import QtMain
from ginga.qtw.ImageViewQt import ImageViewZoom
from ginga import RGBImage

import cv2
import alsaaudio, wave

import remoteObjects as ro

STD_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'


class GingaVision(QtGui.QMainWindow):

    def __init__(self, qtmain, logger, ev_quit, options):
        super(GingaVision, self).__init__()
        self.qtmain = qtmain
        self.logger = logger
        self.ev_quit = ev_quit

        self.card = 'default'

        self.client = ro.remoteObjectClient(options.other, options.port)

        self.queue = Queue.Queue()

        self.pimage = RGBImage.RGBImage()
        self.pdata = None

        fi = ImageViewZoom(self.logger, render='widget')
        fi.enable_autocuts('off')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('off')
        fi.cut_levels(0, 255)
        fi.defer_redraw = False
        fi.set_bg(0.2, 0.2, 0.2)
        # flip y
        fi.transform(False, True, False)
        fi.ui_setActive(True)
        self.fitsimage = fi

        bd = fi.get_bindings()
        bd.enable_pan(False)
        bd.enable_zoom(True)
        bd.enable_cuts(True)
        bd.enable_flip(True)

        w = fi.get_widget()
        w.resize(512, 512)

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

        self.setWindowTitle("Viewer")

        self.setup_audio_input()
        self.setup_audio_output()

    def setup_audio_input(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,
                            self.card)
        inp.setchannels(1)
        inp.setrate(44100)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        #inp.setperiodsize(1024)
        inp.setperiodsize(160)
        self.inp = inp

    def setup_audio_output(self):
        outp = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NONBLOCK,
                             self.card)
        outp.setchannels(1)
        outp.setrate(44100)
        outp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        #outp.setperiodsize(1024)
        outp.setperiodsize(160)
        self.outp = outp

    def quit(self):
        self.logger.info("quit called")
        self.close()
        self.ev_quit.set()

    def show_frame(self, img):
        print("UPDATING IMAGE")
        try:
            if (self.pdata is None) or (img.shape != self.pdata.shape):
                self.pdata = numpy.copy(img)
                self.pimage.set_data(self.pdata)
                self.qtmain.gui_call(self.fitsimage.set_image, self.pimage)
            else:
                self.pimage.set_data(img)
                #self.pdata[::] = img[::]
                #self.qtmain.gui_call(self.fitsimage.redraw)

        except Exception as e:
            self.logger.error("Error unpacking packet: %s" % (
                str(e)))

    def receive_data(self):

        self.logger.info("receive data loop starting...")
        while not self.ev_quit.isSet():
            try:
                item = self.queue.get(block=True, timeout=1.0)
                
            except Queue.Empty:
                continue

            try:
                ## print "buflen1=%d" % len(buf)
                ## idx = buf.index('|')
                ## (wd, ht, dp, bpp, buflen) = map(int, buf[:idx].split(' '))
                ## print "received: %dx%dx%d array %d bpp len %d bytes" % (
                ##     wd, ht, dp, bpp, buflen)
                ## buf = buf[idx+1:]
                ## print "buflen2=%d" % len(buf)

                ## arr = numpy.fromstring(buf, dtype='uint8')
                ## img = arr.reshape((ht, wd, dp))
                img = item['frame']
                self.show_frame(img)
                
            except Exception as e:
                self.logger.error("Error unpacking packet: %s" % (
                    str(e)))

        self.logger.info("receive data loop terminating...")

    def send_data(self):

        self.logger.info("send data loop starting...")
        while not self.ev_quit.isSet():
            try:
                item = self.queue.get(block=True, timeout=0.01)
                
            except Queue.Empty:
                continue

            if self.other is not None:
                (ht, wd, dp) = item['data'].shape
                buf = item['data'].tostring()

                pkt = dict(width=wd, height=ht, depth=dp, bpp=8,
                           imglen=len(buf), imgbuf=buf)
                try:
                    self.client.receive_data(pkt, self.other)
                except Exception as e:
                    continue

        self.logger.info("send data loop terminating...")

    def capture_audio(self):

        self.logger.info("capture audio loop starting...")
        while not self.ev_quit.isSet():
            l, data = self.inp.read()
            #a = numpy.fromstring(data, dtype='int16')
            #print numpy.abs(a).mean()
            #m = self.outp.write(data)
            #print m
            time.sleep(0.01)

        self.logger.info("capture audio loop terminating...")

    def capture_video(self):
        
        self.logger.info("capture video loop starting...")
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture("/home/eric/Videos/star_collapse_out.avi")

        pimage = RGBImage.RGBImage()
        data = None

        while not self.ev_quit.isSet():
            start_time = time.time()
            print("CAPTURE FRAME")
            f, img = cap.read()
            if img is not None:

                data = numpy.copy(img)
                # swap R & B channels, video coming off the cam seems to
                # be in BGR format
                data[:, :, 0] = img[:, :, 2]
                data[:, :, 1] = img[:, :, 1]
                data[:, :, 2] = img[:, :, 0]

                pkt = dict(type=0, frame=data, ts=start_time)
                self.show_frame(data)
                #self.queue.put(pkt)
                        
            end_time = time.time()
            elapsed_time = end_time - start_time
            sleep_time = 0.033333 - elapsed_time

            time.sleep(max(sleep_time, 0.0))
            #cv2.waitKey(1)

        self.logger.info("capture video loop terminating...")


def main(options, args):

    # Set up the logger
    logger = logging.getLogger("example1")
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

    ro.init()
    
    # event for synchronizing exit of all threads
    ev_quit = threading.Event()

    # Create top level of Qt application w/custom event loop
    myqt = QtMain.QtMain(logger=logger, ev_quit=ev_quit)

    gv = GingaVision(myqt, logger, ev_quit, options)
    gv.resize(670, 540)
    gv.show()

    # start video capture thread
    t = threading.Thread(target=gv.capture_video, args=[])
    t.start()
    
    # start audio capture thread
    t = threading.Thread(target=gv.capture_audio, args=[])
    t.start()
    
    # start network listening thread
    t = threading.Thread(target=gv.receive_data, args=[])
    #t.start()
    
    # start network sending thread
    t = threading.Thread(target=gv.send_data, args=[])
    #t.start()
    
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

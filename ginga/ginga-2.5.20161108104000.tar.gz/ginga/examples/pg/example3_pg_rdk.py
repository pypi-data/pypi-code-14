#! /usr/bin/env python
#
# example2_rdk.py -- Test Splitter widget
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from __future__ import print_function
import sys, os
import logging

from ginga import AstroImage, colors
from ginga.canvas.CanvasObject import get_canvas_types
from ginga.misc import log
from ginga.web.pgw import Widgets, Viewers, PgMain

class SplitterTest(object):

    def __init__(self, logger, window):
        self.logger = logger
        self.drawcolors = colors.get_colors()
        self.dc = get_canvas_types()

        self.top = window
        # As of 20151201, closed callback no longer exists, so comment-out next line
        #self.top.add_callback('closed', self.closed)

        # vbox is the container that will hold all the widgets in the
        # page.
        vbox = Widgets.VBox()
        vbox.set_border_width(2)
        vbox.set_spacing(1)

        # Create a Splitter widget with a vertical bar.
        h_splitter = Widgets.Splitter(orientation='horizontal')

        t1 = Widgets.Label('pane 1')
        t2 = Widgets.Label('pane 2')
        #t3 = Widgets.Label('pane 3')

        # Add Label widgets to the h_splitter
        h_splitter.add_widget(t1)
        h_splitter.add_widget(t2)
        #h_splitter.add_widget(t3)

        self.logger.info('1 h_splitter sizes %s' % h_splitter.get_sizes())
        #h_splitter.set_sizes((650,350,200))
        self.logger.info('2 h_splitter sizes %s' % h_splitter.get_sizes())

        # Create a Splitter widget with a horizontal bar.
        v_splitter = Widgets.Splitter(orientation='vertical')

        t4 = Widgets.Label('pane 4')
        t5 = Widgets.Label('pane 5')

        # Add Label widgets to the v_splitter
        v_splitter.add_widget(t4)
        v_splitter.add_widget(t5)

        # Add the v_splitter to the h_splitter
        h_splitter.add_widget(v_splitter)

        # Add the h_splitter to the vbox (overall container)
        vbox.add_widget(h_splitter, stretch=0)

        # Add the vbox (overall container) to the top-level window
        # that we were supplied
        self.top.set_widget(vbox)

    def quit(self, *args):
        self.readout.set_text("Quitting!")
        self.logger.info("Attempting to shut down the application...")
        if not self.top is None:
            self.top.close()
        sys.exit()

def main(options, args):

    logger = log.get_logger("example2", options=options)

    if options.use_opencv:
        from ginga import trcalc
        try:
            trcalc.use('opencv')
        except Exception as e:
            logger.warning("Error using opencv: %s" % str(e))

    base_url = "http://%s:%d/app" % (options.host, options.port)

    # establish our widget application
    app = Widgets.Application(logger=logger,
                              host=options.host, port=options.port)

    #  create top level window
    window = app.make_window("Ginga web example2")

    s = SplitterTest(logger, window)

    #window.show()
    #window.raise_()

    try:
        app.start()

    except KeyboardInterrupt:
        logger.info("Terminating viewer...")
        window.close()

if __name__ == "__main__":

    # Parse command line options with nifty optparse module
    from optparse import OptionParser

    usage = "usage: %prog [options] cmd [args]"
    optprs = OptionParser(usage=usage, version=('%%prog'))

    optprs.add_option("--debug", dest="debug", default=False, action="store_true",
                      help="Enter the pdb debugger on main()")
    optprs.add_option("--host", dest="host", metavar="HOST",
                      default='localhost',
                      help="Listen on HOST for connections")
    optprs.add_option("--log", dest="logfile", metavar="FILE",
                      help="Write logging output to FILE")
    optprs.add_option("--loglevel", dest="loglevel", metavar="LEVEL",
                      type='int', default=logging.INFO,
                      help="Set logging level to LEVEL")
    optprs.add_option("--opencv", dest="use_opencv", default=False,
                      action="store_true",
                      help="Use OpenCv acceleration")
    optprs.add_option("--port", dest="port", metavar="PORT",
                      type=int, default=9909,
                      help="Listen on PORT for connections")
    optprs.add_option("--profile", dest="profile", action="store_true",
                      default=False,
                      help="Run the profiler on main()")
    optprs.add_option("--stderr", dest="logstderr", default=False,
                      action="store_true",
                      help="Copy logging also to stderr")
    optprs.add_option("-t", "--toolkit", dest="toolkit", metavar="NAME",
                      default='qt',
                      help="Choose GUI toolkit (gtk|qt)")

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

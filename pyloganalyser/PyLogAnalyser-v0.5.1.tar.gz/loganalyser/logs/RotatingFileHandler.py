#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
import logging.handlers

DEBUG_DIR = ".debug"


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    Rotating File Handler.
    """

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0):
        """
        Constructor
        """
        basedir = os.path.abspath(os.getcwd())
        #Makedir ".debug"
        logdir = os.path.join(basedir, DEBUG_DIR)
        if not(os.path.isdir(logdir)):
            os.mkdir(logdir)
        logfile = os.path.join(logdir, filename)

        logging.handlers.RotatingFileHandler.__init__(self, logfile, mode, maxBytes, backupCount)

#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
import logging
from logs.RotatingFileHandler import DEBUG_DIR


class FileHandler(logging.FileHandler):
    """
    File Handler
    """

    def __init__(self, filename, mode='a'):
        """
        Constructor
        """
        # Create local directory for storing debug log
        basedir = os.path.abspath(os.getcwd())
        logdir = os.path.join(basedir, DEBUG_DIR)
        if not(os.path.isdir(logdir)):
            os.mkdir(logdir)
        logfile = os.path.join(os.path.abspath(logdir), filename)

        logging.FileHandler.__init__(self, logfile, mode)

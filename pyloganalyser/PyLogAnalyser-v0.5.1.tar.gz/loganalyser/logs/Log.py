#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
import logging
import logging.config
from singleton import Singleton
from setupverbose import logging_file

from RotatingFileHandler import DEBUG_DIR
logging_path = os.path.join(os.getcwd(), DEBUG_DIR, logging_file)

DISABLE_LOG = True
if os.path.exists(logging_path):
    #Enable logging according to logging_file
    DISABLE_LOG = False

#Extra level of 
VERBOSE_number = 5
VERBOSE_str    = 'VERBOSE'
def verbose(self, message, *args, **kws):
    '''
    '''
    self.log(VERBOSE_number, message, *args, **kws)

@Singleton
class debugLog(object):
    """
    """

    def __init__(self):
        """
        """
        #
        if not(DISABLE_LOG):
            logging.addLevelName(VERBOSE_number, VERBOSE_str)
            logging.Logger.verbose = verbose
            logging.config.fileConfig(logging_path)

    def get_logger(self, name):
        """
        Get logger with name
        """
        logger = logging.getLogger(name)
        #logger.disabled = True
        if DISABLE_LOG:
            from dummylogger import DummyLogger
            logger = DummyLogger()

        return logger

'''
REF:
http://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
'''

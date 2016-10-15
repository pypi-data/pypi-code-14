#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
from ConfigParser import RawConfigParser
from RotatingFileHandler import DEBUG_DIR
import shutil

logging_file = "logging.conf"

def setupverbose(verbose):
    """
    """
    base_dir = os.path.join(os.getcwd(), DEBUG_DIR)

    # For debug logging, 
    #  create directory if does not exist and
    #  verbose is not None, then
    #  copy logging.conf to new destination
    #  to edit it.
    logging_path_dst = os.path.join(base_dir, logging_file)
    if os.path.exists(logging_path_dst) and \
       (verbose is None):
        # Remove file is exists from previous runs
        #  but verbose is None in current run
        os.remove(logging_path_dst)

    if verbose is not None:
        if not(os.path.exists(base_dir)): os.mkdir(base_dir)
        #copy logging conf
        folder_path = os.path.dirname(os.path.abspath(__file__))
        logging_path_src = os.path.join(folder_path, logging_file)
        if not(os.path.exists(logging_path_dst)): shutil.copy2(logging_path_src, logging_path_dst)
    else:
        return

    # Open this logging_file and edit it according to
    #  verbose option.
    logging_conf = RawConfigParser()
    #print logging_path
    logging_conf.readfp(open(logging_path_dst))

    if verbose == "log":
        logging_conf.set("handlers", "keys", "hfile")
        logging_conf.set("logger_root", "handlers", "hfile")
    elif verbose == "console":
        logging_conf.set("handlers", "keys", "hconsole")
        logging_conf.set("logger_root", "handlers", "hconsole")
    elif verbose == "both":
        logging_conf.set("handlers", "keys", "hconsole,hfile")
        logging_conf.set("logger_root", "handlers", "hconsole,hfile")

    # The changes are saved.
    logging_conf.write(open(logging_path_dst, "w"))

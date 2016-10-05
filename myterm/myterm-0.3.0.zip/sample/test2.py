#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test of myterm.StreamHandler
"""

import os
import logging
import logging.handlers
import myterm

VERSION="0.1"
PROG="test1"
DESCRIPTION="""test of myterm.StreamHandler"""
AUTHOR="Frederic Aoustin"

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = myterm.OptionParser(version="%s %s" % (PROG,VERSION), usage=usage)
    parser.description= DESCRIPTION
    parser.epilog = AUTHOR
    try:
        (options, args) = parser.parse_args()
        # create logger
        logger = logging.getLogger("simple_example")
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = myterm.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter("%(icon)s %(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)

        # "application" code
        logger.debug("debug message")
        logger.info("info message")
        logger.warn("warn message")
        logger.error("error message")
        logger.critical("critical message")

    except Exception as e:
        parser.error(e)
        sys.exit(1)

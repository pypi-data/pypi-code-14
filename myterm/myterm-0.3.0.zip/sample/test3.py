#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test of myterm.Logger
"""

import os
import myterm
import myterm.log

VERSION="0.1"
PROG="test3"
DESCRIPTION="""test of myterm.Logger"""
AUTHOR="Frederic Aoustin"

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = myterm.OptionParser(version="%s %s" % (PROG,VERSION), usage=usage)
    parser.description= DESCRIPTION
    parser.epilog = AUTHOR
    try:
        (options, args) = parser.parse_args()
        # create logger
        logger= myterm.Logger(level=myterm.log.LEVELLOG["DEBUG"])
        logger.add_stream()

        # "application" code
        logger.debug("debug message")
        logger.info("info message")
        logger.warn("warn message")
        logger.error("error message")
        logger.critical("critical message")

    except Exception as e:
        parser.error(e)
        sys.exit(1)

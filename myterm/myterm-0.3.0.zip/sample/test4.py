#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test of myterm.parser manage conf
"""
import sys
import os
import myterm
import myterm.log
from myterm.parser import find_confdir

VERSION="0.1"
PROG="test4"
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
        logger.info('conf exist and ok')
        d, f, conf = find_confdir("conf")
        logger.debug("value of test: %s" % getattr(conf, 'test', 'bye'))
        logger.debug("value of testtwo: %s" % getattr(conf, 'testtwo', 'bye'))
        try:
            logger.info('conf exist and wrong')
            d, f, conf = find_confdir("confwrong")
            print(getattr(conf, 'test', 'bye'))
        except Exception as e:
            logger.critical(e)
        logger.info('conf not exist')
        d, f, conf = find_confdir("confnotexist")
        print(getattr(conf, 'test', 'bye'))
    except Exception as e:
        parser.error(e)
        sys.exit(1)

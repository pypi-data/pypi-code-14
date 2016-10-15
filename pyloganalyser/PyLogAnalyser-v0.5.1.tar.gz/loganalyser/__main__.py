#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Main script to be used from command line with \'python -m\'
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
import sys
from __optparse__ import parseinput


def main():
  """
  """

  (options, args) = parseinput()

  #Setup the logger
  from logs.setupverbose import setupverbose
  setupverbose(options.verbose)

  from logs.loggers import LOGGER_MAIN
  logger = LOGGER_MAIN

  from PyLogAnalyser import LogAnalyser

  from __optcheck__ import checkinput
  (options, consistent) = checkinput(options)
  if not(consistent): return

  logger.info("*** MODULE BEGIN ***")

  #Print system variables
  logger.info( "--- LOGANALYSER PARAMETERS ---")
  logger.info( "Input file: %s " % options.input_file )
  logger.info( "Output file: %s " % options.output_file )
  logger.info( "Configuration file: %s " % options.conf_file )
  logger.info( "Stdin option: %s " % options.stdin )
  logger.info( "Stdout option: %s " % options.stdout )
  logger.info("------------------------------")

  #Instantiate log Analyser class
  logger.debug("LogAnalyser class to be instantiated")
  logAnalyser = LogAnalyser(input = options.input_file, \
                            output = options.output_file, \
                            conf = options.conf_file, \
                            stdin = options.stdin, \
                            stdout = options.stdout)
  logger.debug("LogAnalyser class instantiated")

  logAnalyser.run()

  logger.info("*** MODULE END ***")

if __name__ == "__main__":
  """
  """
  #name [-i <input> -n|--stdin] [-o <output> -u|--stdout] -c <conf> -v [log|console|both] -h|--help
  sys.exit( main() )

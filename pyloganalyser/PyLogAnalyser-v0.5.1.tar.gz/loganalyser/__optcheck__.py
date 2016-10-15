#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Module that checks input parameters provided by the user from the __main__.py module
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
from logs.loggers import LOGGER_MAIN

#System variables
LOGANA_IN = "LOGANA_IN"
LOGANA_OUT = "LOGANA_OUT"
LOGANA_CONF = "LOGANA_CONF"


def checkinput(options):
  """
  It checks if options are consistent or not.

  Returns tuple(options, consistent) where options are
  ouput options and consistent is boolean value.
  True is data ok, False is data unconsistent and
  execution should be stopped.
  """
  logger = LOGGER_MAIN

  consistent = True
  #
  #Make exclusion check in case of
  #  about, report and demo appear.
  condition_1 = (options.about is True) and \
                (options.report is True) and \
                (options.demo is True)
  condition_2 = (options.about is True) and \
                ((options.report is True) or \
                (options.demo is True))
  condition_3 = (options.report is True) and \
                ((options.about is True) or \
                (options.demo is True))
  condition_4 = (options.demo is True) and \
                ((options.about is True) or \
                (options.report is True))

  if condition_1 or condition_2 or \
     condition_3 or condition_4:
     msg = "This options are mutually exclusive.\n" + \
           " Please, use them alone, just one of them.\n"
     print(msg)
     return (options, False)

  if options.about is True:
     from __display__ import about_msg
     print about_msg
     return (options, False)

  if options.report is True:
    from __display__ import how_to_report
    print how_to_report()
    return (options, False)

  if options.demo is True:
    from __display__ import show_demo
    print show_demo()
    return (options, False)

  #Check that verbose is a valid value
  from __optparse__ import VERBOSE_LOG, VERBOSE_CON, VERBOSE_BOTH
  if (options.verbose is not None) and \
     (options.verbose != VERBOSE_LOG) and \
     (options.verbose != VERBOSE_CON) and \
     (options.verbose != VERBOSE_BOTH):
     msg = "Invalid \'verbose\' option.\n" + \
           " Please, use one of the three possibles: " + \
           " %s, %s or %s \n" % (VERBOSE_LOG, VERBOSE_CON, VERBOSE_BOTH)
     print(msg)
     return (options, False)

  if (options.verbose == VERBOSE_CON) and \
     (options.stdout):
    #
    msg = "\n" + \
          "Invalid options:\n" + \
          " The system should not print by the standard output\n" + \
          " the filtered messages and the debug logs.\n" + \
          "Please, either print the filtered messages by other \n" + \
          " output or save the debug logs in a file.\n"
    print(msg)
    return (options, False)

  #Check no inconsistencies in arguments:
  if (options.input_file is not None) \
      and (options.stdin):
    print("Wrong input. For input, use either an input file\n \
        or the standard input, but not both.")
    return (options, False)

  #Raise exception if no input is provided
  if (options.input_file is None) \
      and (os.getenv(LOGANA_IN) is None) \
      and (options.stdin == False):
    print("No input has been especified. Please\n \
        indicate either input by file, system variable or\n \
        standard input.")
    return (options, False)

  #If not present, take them from system_variables.
  #System variables
  #Use LOGANA_IN is not None
  if (options.input_file is None) \
      and (os.getenv(LOGANA_IN) is not None) \
      and (options.stdin == False):
    logger.debug("Input file taken from system variable")
    options.input_file = os.getenv(LOGANA_IN)

  #Raise exception if no output is provided
  if (options.output_file is None) \
      and (os.getenv(LOGANA_OUT) is None) \
      and (options.stdout == False):
    print("No output has been especified. Please\n \
        indicate either output by file, system variable or\n \
        standard output.")
    return (options, False)

  #Use LOGANA_OUT is not None
  if (options.output_file == None) \
      and (os.getenv(LOGANA_OUT) is not None) \
      and (options.stdout == False):
    logger.debug("Output file taken from system variable")
    options.output_file = os.getenv(LOGANA_OUT)

  #Raise exception if no configuration is provided
  if (options.conf_file == None) \
    and (os.getenv(LOGANA_CONF) == None):
    #
    print("No configuration has been especified.\n \
        Please indicate configuration either by file or system variable.")
    return (options, False)

  #Use LOGANA_CONF is configuration is None
  if (options.conf_file == None) \
    and (os.getenv(LOGANA_CONF) != None):
    #
    logger.debug("Configuration file taken from system variable")
    options.conf_file = os.getenv(LOGANA_CONF)

  #Check that the files actually exists.
  #Check input file
  file_no = 1
  if (options.input_file is not None):
      try:
        f = open(options.input_file, "r")
        f.close()
      except IOError, e:
        msg = "The input file [%s] does not exist, \n" % file_no + \
              " please, provide the right path to it.\n" + \
              "\n" + \
              " [%s] %s \n" % (file_no, str(options.input_file))
        print(msg)
        file_no += 1
        consistent = False

  #Check output file
  if (options.output_file is not None):
      try:
        f = open(options.output_file, "r")
        msg = "The output file \"%s\" already exist, " % options.output_file + \
              " it will be overwritten"
        logger.warning(msg)
        f.close()
      except IOError, e:
        pass

  #Check conf file
  if (options.conf_file is not None):
      try:
        f = open(options.conf_file, "r")
        f.close()
      except IOError, e:
        msg = "The configuration file [%s] does not exist, \n" % file_no + \
              " please, provide the right path to it.\n" + \
              "\n" + \
              " [%s] %s \n" % (file_no, str(options.conf_file))
        print(msg)
        consistent = False

  return (options, consistent)

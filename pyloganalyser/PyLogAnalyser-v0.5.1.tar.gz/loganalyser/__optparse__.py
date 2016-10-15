#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Module that parses the input parameters provided by the user from the __main__.py module
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

from optparse import OptionParser
from __init__ import __package__, __version__

VERBOSE_LOG  = "log"
VERBOSE_CON  = "console"
VERBOSE_BOTH = "both"

def parseinput():
  """
  Function that parses all the input parameters
   provided by the user from the command line.

  Returns a tuple of (options, args).
  """
  #Option parser:
  usage_string = "python -m loganalyser [-i] [-o] [-c] [-t] [-d|--demo] [-r|--report] [-b|--about] [-n|--stdin] [-u|--stdout]"
  parser = OptionParser(usage = usage_string, \
                        version = " %s %s." % (__package__, __version__))

  parser.add_option("-v", "--verbose", dest="verbose",
    type="string",
    help="Three possible values:" + \
         "\'%s\' saves logs in file;" % (VERBOSE_LOG) + \
         "\'%s\' shows in console;" % (VERBOSE_CON) + \
         "\'%s\' does both;" % (VERBOSE_BOTH),
    metavar="[log|console|both]")

  parser.add_option("-i", "--input", dest="input_file", \
    type="string",
    help="Input file to parse (LOGANA_IN by default)",
    metavar="FILE")

  parser.add_option("-o", "--output", dest="output_file",
    type="string", #type by default
    help="output file where to write (LOGANA_OUT by default)",
    metavar="FILE")

  parser.add_option("-c", "--conf", dest="conf_file",
    type="string", #type by default
    help="configuration file containing rules to apply (LOGANA_CONF by default)",
    metavar="FILE")

  #Add the about information
  parser.add_option("-b", "--about",
    action="store_true",
    default=False,
    help="Displays information about the tool",
    dest="about")

  #Add the demo information
  parser.add_option("-s", "--demo",
    action="store_true",
    default=False,
    help="Shows instructions on how to use PyLogAnalyser",
    dest="demo")

  #Add the report information
  parser.add_option("-r", "--report",
    action="store_true",
    default=False,
    help="Displays information about how to report an issue",
    dest="report")

  #stdin: Store True and False#
  stdin_help = "Uses stdin providing line inputs."
  parser.add_option("-n", "--stdin",
    action="store_true",
    default=False,
    help=stdin_help,
    dest="stdin")

  #Store True and False#
  stdout_help = "Uses stdout for printing results."
  parser.add_option("-u", "--stdout",
    action="store_true",
    default=False,
    help=stdout_help,
    dest="stdout")

  (options, args) = parser.parse_args()

  return (options, args)

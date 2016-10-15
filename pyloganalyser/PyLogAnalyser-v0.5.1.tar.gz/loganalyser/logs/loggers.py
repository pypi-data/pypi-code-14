#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Loggers from Log.py script to be imported from the different scripts
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

from loganalyser.logs.Log import debugLog

LOGGER_MAIN     = debugLog.get_instance().get_logger("__main__")
LOGGER_PyLogAn  = debugLog.get_instance().get_logger("PyLogAnalyser")
LOGGER_RULESET  = debugLog.get_instance().get_logger("Ruleset")
LOGGER_RULE     = debugLog.get_instance().get_logger("Rule")

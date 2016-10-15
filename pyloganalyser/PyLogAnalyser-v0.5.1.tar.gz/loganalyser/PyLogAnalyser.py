#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      PyLogAnalyser module used from __main__.py module
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
import sys
import re
from Ruleset import Ruleset
from Document import Document
from handler.StdoutHandler import StdoutHandler
from handler.TxtHandler import TxtHandler
from handler.HTMLHandler import HTMLHandler
from logs.loggers import LOGGER_PyLogAn


class LogAnalyser(object):
    """
    """
    #End of Readline
    EORL = ''

    #Type of output
    TXT_FILE = ".LOG"
    TXT_FILE_regex = re.compile(r"\.LOG|\.TXT")
    HTML_FILE = ".HTML"
    BOTH_FILES = ".BOTH"

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        @param input: input file to analyze, stdin if not present.
        @type input: string or None.

        @param output: output file to analyze, stdout if not present.
        @type output: string or None.

        @param conf: configuration file containing the rules to follow.
        @type conf: string.

        @param help: it prints the help of the class.
            This option disables the rest of the options.
        @type help: string.
        """
        #
        self._logger = LOGGER_PyLogAn
        self._logger.info("*** class LogAnalyser BEGIN ***")

        #Set input parameters
        self.__conf = None
        self.__input = None
        self.__stdin = None
        self.__input_fd = None
        self.__input_line = None
        self.__input_counter = int(0)
        self.__output = None
        self.__type_of_output = None
        self.__handlers = list([])
        self.__document = Document()
        self.__stdout = None

        #Read from the dictionary
        self._logger.verbose("Arguments to be read")
        self.__conf     = kwargs["conf"]
        self.__input    = kwargs["input"]
        self.__stdin    = kwargs["stdin"]
        self.__output   = kwargs["output"]
        self.__stdout   = kwargs["stdout"]
        self._logger.debug("Arguments read")

        #Read file
        self.__read_input_file()
        self._logger.debug("Input file read")

        #Set attributes
        self._logger.debug("Ruleset object to be instantiated")
        self.__ruleset = Ruleset(self.__conf)
        self._logger.info("Ruleset object instantiated")
        self._logger.info("Ruleset: %s" % str(self.__ruleset))

    def __read_input_file(self):
        """
        Reads and loads input file.
        """
        try:
            if not(self.__stdin):
                self._logger.debug("Input from file")
                self.__input_fd = file(self.__input)
            elif self.__stdin:
                self._logger.debug("Input from stdin")
                self.__input_fd = sys.stdin

        except Exception:
            raise Exception("There were a exception " +
                "reading input file. Please, check.")

    def __next_iter(self):
        """
        Returns True if there are still lines to parse.
        In case of tailing, it always return True.

        @return: True if there are yet lines to parse.
        @rtype: Boolean.
        """
        self._logger.debug("Next line to be read")
        #Reassign variables to easen names.
        input = self.__input
        input_ctr = self.__input_counter

        #Result
        result = None

        #Read lines
        line_read = self.__input_fd.readline()

        EORL = LogAnalyser.EORL
        if (line_read == EORL):
            self._logger.verbose("Line read is EORL")
            result = False
        elif (line_read != EORL):
            self._logger.verbose("Read next input line and counter")
            self.__input_line = line_read
            self.__input_counter += 1
            result = True
        else:
            raise Exception("There were an error while next iteration.")

        self._logger.verbose("Next iteration goes on?: %s " % str(result))
        self._logger.verbose("Reading next line ends")
        return result

    def run(self):
        """
        """
        self._logger.info("Processing lines begin")
        input_line  = self.__input_line
        input_ctr   = self.__input_counter
        stdout      = self.__stdout

        document = self.__document
        handlers = self.__handlers
        # TODO: both 'if stdout' and
        #  if self.__output
        #Set handlers
        if stdout:
            self._logger.verbose("stdout handler instantiation")
            stdout_hdlr = StdoutHandler()
            handlers.append(stdout_hdlr)
            document.add_handler(stdout_hdlr)
            self._logger.debug("stdout handler instantiated")

        if self.__output:
            #Get handlers and add it to the document
            self.__process_output()

        try:
            self._logger.verbose("Loop to begin")
            while self.__next_iter():
                self._logger.verbose("Loop begins")
                #Renaming for easier use.
                ruleset = self.__ruleset
                input_line = self.__input_line

                self._logger.debug("Input line: %s" % str(input_line))
                input_ctr  = self.__input_counter
                self._logger.debug("Input Counter: %s" % str(input_ctr))

                #Process the read line through ruleset
                line = input_line
                line_number = input_ctr
                #Ruleset devuelve un objeto linea
                # y linea se adjunta a clase documento
                # y ya existe previamente un objeto documento
                self._logger.debug("Ruleset: get output")
                log_line = ruleset.get_output(line, line_number)
                self._logger.debug("Ruleset: output: %s" % str(log_line))

                #Conceive the case where multiple log_lines
                # can be generated, because of 'lines_after'
                # parameter present.

                if log_line is not None:
                    self._logger.debug("Append new log line to document")
                    document.append(log_line)
                    self._logger.debug("New log line appended")

                self._logger.debug("Loop ends")

            self._logger.debug("Loop finished")
        except KeyboardInterrupt, key_interr:
            msg = "Keyboard interruption detected!"
            self._logger.warning(msg)
            #FIXME: Document should reset console
            #  foreground and background colours
            #  in case that log_line changes it
            #  (this is a very corner case)
            document.close()
            print msg
            print key_interr

        document.close()
        self._logger.info("Processing lines end")

    def __process_output(self):
        """
        """
        self._logger.verbose("Output file setup begins")
        document = self.__document
        handlers = self.__handlers

        self.__type_of_output = self.__get_type_of_output()
        type_of_output = self.__type_of_output
        self._logger.verbose("Type of output: %s" % str(type_of_output))
        if bool(LogAnalyser.TXT_FILE_regex.match(type_of_output)):
            self._logger.verbose("TxtHandler instantiation")
            file_hdlr = TxtHandler(self.__output)
            handlers.append(file_hdlr)
            self._logger.debug("TxtHandler instantiated and appended")
        elif type_of_output == LogAnalyser.HTML_FILE:
            self._logger.verbose("HTMLHandler instantiation")
            file_hdlr = HTMLHandler(self.__output)
            handlers.append(file_hdlr)
            self._logger.debug("HTMLHandler instantiated and appended")
        elif type_of_output == LogAnalyser.BOTH_FILES:
            self._logger.verbose("HTML and File handlers instantiation")
            (txt_output, html_output) = self.__get_both_outputs()
            file_hdlr = TxtHandler(txt_output)
            handlers.append(file_hdlr)
            html_hdlr = HTMLHandler(html_output)
            handlers.append(html_hdlr)
            self._logger.debug("HTML and Text handlers instantiated and appended")

        for handler in handlers:
            self._logger.verbose("Append handlers to document")
            document.add_handler(handler)
            self._logger.debug("Document handlers appended")

        self._logger.debug("Output file setup ends")

    def __get_type_of_output(self):
        """
        """
        (dirpath, basefile) = os.path.split(self.__output)
        (filename, ext) = os.path.splitext(basefile)

        #Raise exception if no TXT nor HTML
        return ext.upper()

    def __get_both_outputs(self):
        """
        """
        txt_output = None
        html_output = None

        (dirpath, basefile) = os.path.split(self.__output)
        (filename, ext) = os.path.splitext(basefile)

        txt_output = filename + LogAnalyser.TXT_FILE
        txt_output = os.path.join(dirpath, txt_output)

        html_output = filename + LogAnalyser.HTML_FILE
        html_output = os.path.join(dirpath, html_output)

        return (txt_output, html_output)

    def __del__(self):
        """
        Destructor
        """
        self._logger.info("*** class LogAnalyser END ***")

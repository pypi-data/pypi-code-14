# -*- coding: utf-8 -*-

import os
import sys
import select

from .input_base import InputBase
from ...utils.utilty import Utility

THREAD_STOPFLAG_WAIT = 0.000001 # in seconds

class FileInput(InputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.__logFileHandler = None

    def startupCheck(self):
        if not os.access(self.options.logFilePath, os.R_OK):
            Utility.eprint("Error: Input file " + self.options.logFilePath + " not readable. Exiting...")
            sys.exit(1)


    def startUp(self):
        try:
            self.__logFileHandler = open(self.options.logFilePath, 'r')
        except IOError:
            Utility.eprint("Error: Input file " + self.options.logFilePath + " not readable. Exiting...")
            sys.exit(1)
        else:
            if(self.options.debug):
                print("Openend file '" + self.options.logFilePath + "'")

    def tearDown(self):
        self.__logFileHandler.close()
        if(self.options.debug):
            print("Closed file '" + self.options.logFilePath + "'")

    def retrieveNewSamples(self):
        inputready,outputready,exceptready = select.select([self.__logFileHandler.fileno()],[],[])
        for s in inputready:
            if(s == self.__logFileHandler.fileno()):
                tmpBuffer = []
                for line in self.__logFileHandler:

                    #ignore comments
                    if not line.startswith("#"):
                        line = line.strip()
                        tmpBuffer.append(line,)

        return tmpBuffer

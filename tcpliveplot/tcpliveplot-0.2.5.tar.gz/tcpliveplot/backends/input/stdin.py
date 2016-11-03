# -*- coding: utf-8 -*-

from .input_base import InputBase

class StdinInput(InputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry

    def startupCheck(self):
        pass


    def startUp(self):
        pass

    def tearDown(self):
        pass

    def retrieveNewSamples(self):
        pass

# -*- coding: utf-8 -*-

import sys

from pyATK.Cmd.Console.InputArgument import InputArgument
from pyATK.Cmd.Console.InputOption import InputOption
from pyATK.Cmd.Console.Input import Input
from pyATK.Cmd.Console.Output import Output


class BaseApplication:
    """
    >>> myApp = BaseApplication()
    >>> myApp.setName("Test App")
    <pyATK.Cmd.Base.BaseApplication.BaseApplication object at 0x...>
    >>> myApp.setVersion("0.0.1")
    <pyATK.Cmd.Base.BaseApplication.BaseApplication object at 0x...>
    >>> myApp.addArgument("argument", "argument description")
    <pyATK.Cmd.Base.BaseApplication.BaseApplication object at 0x...>
    >>> myApp.addOption("o", "option", "option description")
    <pyATK.Cmd.Base.BaseApplication.BaseApplication object at 0x...>
    """

    STATUS_SUCCESS = 0x0
    STATUS_FAILURE = 0x1

    def __init__(self):
        self.name = ""
        self.version = ""
        self.expectingOptions = False
        self.expectingArguments = False
        self.input = Input()
        self.output = Output()

    def setName(self, name):
        self.name = name
        return self

    def setVersion(self, version):
        self.version = version
        return self

    def addOption(self, shortForm, longForm=None, description=None, optionRequired=InputOption.OPTION_NONE):
        newOption = InputOption(shortForm, longForm, description, optionRequired)
        self.input.registerOption(newOption)
        return self

    def addArgument(self, argumentName, description, mode=InputArgument.ARGUMENT_REQUIRED, type_=str, defaultValue=None):
        newArgument = InputArgument(argumentName, description, mode=mode, defaultValue=defaultValue, type_=type_)
        self.input.registerArgument(newArgument)
        return self

    def run(self):
        self.doConfigure()

        self.input.parse(sys.argv)
        self.doRun()
        sys.exit(self.STATUS_SUCCESS)

        # except Exception as err:
        #     print(err)
        #     return self.STATUS_FAILURE

    def doConfigure(self):
        raise NotImplementedError("This method is not implemented!")


    def doRun(self):
        raise NotImplementedError("This method is not implemented!")

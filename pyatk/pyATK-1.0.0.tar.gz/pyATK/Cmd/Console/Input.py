# -*- coding: utf-8 -*-
import argparse
from pyATK.Cmd.Console.InputOption import InputOption
from pyATK.Cmd.Console.InputArgument import InputArgument
from pyATK.Cmd.Helpers.ArgumentsHelper import ArgumentsHelper


class Input:
    """
    >>> input = Input()
    >>> arg = InputArgument("first-argument", "")
    >>> input.registerArgument(arg)
    >>> opt = InputOption("help", "null description", InputOption.OPTION_REQUIRED)
    >>> input.registerOption(opt)
    >>> input.getOption(opt.longForm)
    """

    HELP_REQUIRED = 0x01

    def __init__(self):
        self.argumentsHelper = ArgumentsHelper(self)
        self.arguments = []
        self.options = []
        self.parser = argparse.ArgumentParser()

    def getArgument(self, argName):
        return self.argumentsHelper.argument(argName).value

    def registerArgument(self, argument):
        self.arguments.append(argument)
        self.parser.add_argument(argument.name, type=argument.type, default=argument.value, nargs=argument.mode)

    def getOption(self, optName):
        return self.argumentsHelper.option(optName).value

    def registerOption(self, option):
        self.options.append(option)
        if option.optionRequired == InputOption.OPTION_NONE:
            self.parser.add_argument(option.shortForm, option.longForm, action="store_true")
        else:
            self.parser.add_argument(option.shortForm, option.longForm)


    def parse(self, cli_args):
        parsed = self.parser.parse_args(cli_args[1:])
        for option in self.options:
            if hasattr(parsed, option.name):
                option.setValue(getattr(parsed, option.name))

        for argument in self.arguments:
            if hasattr(parsed, argument.name):
                argument.setValue(getattr(parsed, argument.name))


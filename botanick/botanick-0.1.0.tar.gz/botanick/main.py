# -*- coding: UTF-8 -*-

from commands.parser import Parser
from const import SPLASH


if __name__ == "__main__":
    """
    """
    print(SPLASH)
    try:
        parser = Parser()
        command = parser.getCommand()
        args = parser.getArgs()
        if not args:
            command()
        else:
            command(args)
    except KeyboardInterrupt:
        print('Execution aborted by user ! Bye !')

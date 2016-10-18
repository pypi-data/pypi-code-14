#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from traceback import format_exc

from prompt_toolkit import prompt

from j1bz.expression.interpreter import interpret
from j1bz.expression.exceptions import ParserGenerationError, ParseError


def cli_interpreter():
    print("=== Expression CLI interpreter ===")
    print("Enter 'QUIT' to quit")
    print("")

    cmd = ''
    while True:
        try:
            cmd = prompt('> ')

        except EOFError:
            break

        except KeyboardInterrupt:
            break

        if cmd == 'QUIT':
            break

        try:
            res = interpret(cmd)

        except (ParserGenerationError, ParseError) as e:
            print(format_exc(e))
            continue

        print(repr(res))


def main():
    cli_interpreter()


if __name__ == '__main__':
    main()

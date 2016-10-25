#!/bin/env python

from cement.core.foundation import CementApp
from controller import DOController
from base import BaseController


class PyDOTool(CementApp):
    class Meta:
        label = 'pydotool'

        handlers = [
            BaseController,
            DOController
        ]


def main():
    with PyDOTool() as app:
        app.log.set_level('INFO')
        app.run()

if __name__ == '__main__':
    main()


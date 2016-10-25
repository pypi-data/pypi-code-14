#!/bin/env python

import os
from cement.core.foundation import CementApp
from controller import DOController
from base import BaseController


class ImoneyDO(CementApp):
    class Meta:
        label = 'imoney-do'
        config_files = [os.path.dirname(os.path.realpath(__file__)) + '/app.conf']

        handlers = [
            BaseController,
            DOController
        ]


def main():
    with ImoneyDO() as app:
        app.log.set_level('INFO')
        app.run()

if __name__ == '__main__':
    main()


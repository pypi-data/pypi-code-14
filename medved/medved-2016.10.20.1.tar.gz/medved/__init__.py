#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from medved.controller import MedvedController


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('medved')
    MedvedController()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

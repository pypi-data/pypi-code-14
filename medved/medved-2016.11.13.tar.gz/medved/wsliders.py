#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from .ui.ui_sliders import Ui_QSlidersWidget


class WSliders(QtWidgets.QWidget, Ui_QSlidersWidget):
    def __init__(self, plot, parent):
        super().__init__(parent)
        self._parent = parent
        self.plot = plot
        self.setupUi(self)

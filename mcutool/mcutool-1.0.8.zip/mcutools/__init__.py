#!/usr/bin/env python
# _*_ coding=gbk _*_

import wx
from mcutools import gui

def main(args=None):
    app = wx.App()
    gui.MyFrame()
    app.MainLoop() 
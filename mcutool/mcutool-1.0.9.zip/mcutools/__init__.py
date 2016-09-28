#!/usr/bin/env python
# _*_ coding=gbk _*_

try:
    import wx
except ImportError:
    print "mcutool requires wxPython which is missing from your system"
    print "wxPython currently does not use distutils so is not automatically installed"
    print "you can install wxPython by visiting http://www.wxpython.org"
    raise
from mcutools import gui

def main(args=None):
    app = wx.App()
    gui.MyFrame()
    app.MainLoop() 
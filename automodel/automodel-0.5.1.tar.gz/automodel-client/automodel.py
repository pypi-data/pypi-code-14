#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import window.main_window as main_window

modules ={u'main_window': [1, 'Main frame of Application', u'main_window.py'],
 'sequece_window': [0, '', u'sequece_window.py'],
 u'alinhar_window': [0, '', u'alinhar_window.py'],
 u'loop_window': [0, '', u'loop_window.py'],
 u'modelar_window': [0, '', u'modelar_window.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = main_window.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()

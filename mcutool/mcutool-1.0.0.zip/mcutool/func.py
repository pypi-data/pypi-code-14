#!/usr/bin/env python
# _*_ coding=gbk _*_

import os.path 
import wx

def check_file_exist(tc,check):
    if check:
        filepath = tc.GetValue()
        if os.path.exists(filepath) and os.path.isfile(filepath):
            #tc.SetBackgroundColour((10,255,10,10))
            return True
        else:
            #tc.SetBackgroundColour((255,50,50,255))
            return False
    else:
        return True
    
def set_file_path(pp,tc):
    wildcard = "Binary file (*.bin)|*.bin|"\
        "All files (*.*)|*.*"
    dialog = wx.FileDialog(None, u"选择文件", os.getcwd(), 
            "", wildcard, wx.OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        binpath=dialog.GetPath()
        tc.SetValue(binpath)
        #tc.SetBackgroundColour((10,255,10,10))

    dialog.Destroy()    

def message_box(title_str,warning_str):
    dlg = wx.MessageBox(parent=None, message=warning_str,
                          caption=title_str,
                          style=wx.OK)# | wx.ICON_QUESTION)
    #print "test dlg : ",dlg

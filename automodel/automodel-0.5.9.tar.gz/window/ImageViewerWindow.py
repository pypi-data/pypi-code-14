#Boa:Frame:ImageViewer

import shutil
import os
import wx

def create(parent):
    return ImageViewer(parent)

[wxID_IMAGEVIEWER, wxID_IMAGEVIEWERPANEL1, wxID_IMAGEVIEWERSAVEASBUTTON, 
 wxID_IMAGEVIEWERSTATICBITMAP1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class ImageViewer(wx.Frame):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.SaveAsButton, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.staticBitmap1, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.panel1.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_IMAGEVIEWER, name=u'ImageViewer',
              parent=prnt, pos=wx.Point(320, 175), size=wx.Size(748, 439),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Image Viewer')
        self.SetClientSize(wx.Size(760, 700))

        self.panel1 = wx.Panel(id=wxID_IMAGEVIEWERPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(748, 439),
              style=wx.TAB_TRAVERSAL)

        self.SaveAsButton = wx.Button(id=wxID_IMAGEVIEWERSAVEASBUTTON,
              label=u'Save As...', name=u'SaveAsButton', parent=self.panel1,
              pos=wx.Point(10, 10), size=wx.Size(85, 27), style=0)
        self.SaveAsButton.Bind(wx.EVT_BUTTON, self.OnSaveAsButtonButton,
              id=wxID_IMAGEVIEWERSAVEASBUTTON)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_IMAGEVIEWERSTATICBITMAP1, name='staticBitmap1',
              parent=self.panel1, pos=wx.Point(0, 47), size=wx.Size(730, 647),
              style=0)

        self._init_sizers()

    def __init__(self, parent, text_file_name):
        self._init_ctrls(parent)
        self.text_file_name = text_file_name
        self.png = self.__loadImage__()
        self.staticBitmap1.SetBitmap(self.png)

    def OnSaveAsButtonButton(self, event):
        dialog = wx.FileDialog(None, "Save in", defaultFile= self.text_file_name,
          style=wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
          shutil.copyfile(self.text_file_name, dialog.GetPath())

    def __loadImage__(self):
      return wx.Image(self.text_file_name, wx.BITMAP_TYPE_ANY).ConvertToBitmap()




#Boa:Dialog:AboutAutoModel

import wx

def create(parent):
    return AboutAutoModel(parent)

[wxID_ABOUTAUTOMODEL, wxID_ABOUTAUTOMODELAUTOMODELNAME, 
 wxID_ABOUTAUTOMODELBUTTONOK, wxID_ABOUTAUTOMODELSTATICTEXT1, 
 wxID_ABOUTAUTOMODELSTATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(5)]

class AboutAutoModel(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_ABOUTAUTOMODEL, name=u'AboutAutoModel',
              parent=prnt, pos=wx.Point(428, 305), size=wx.Size(395, 222),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'About AutoModel')
        self.SetClientSize(wx.Size(395, 222))

        self.buttonOk = wx.Button(id=wxID_ABOUTAUTOMODELBUTTONOK, label=u'OK',
              name=u'buttonOk', parent=self, pos=wx.Point(160, 176),
              size=wx.Size(85, 27), style=0)
        self.buttonOk.Bind(wx.EVT_BUTTON, self.OnButtonOkButton,
              id=wxID_ABOUTAUTOMODELBUTTONOK)

        self.automodelName = wx.StaticText(id=wxID_ABOUTAUTOMODELAUTOMODELNAME,
              label=u'AutoModel version 0.5', name=u'automodelName',
              parent=self, pos=wx.Point(124, 22), size=wx.Size(147, 17),
              style=0)

        self.staticText1 = wx.StaticText(id=wxID_ABOUTAUTOMODELSTATICTEXT1,
              label=u'Copyright 2009-2014', name='staticText1', parent=self,
              pos=wx.Point(128, 136), size=wx.Size(137, 17), style=0)

        self.staticText2 = wx.StaticText(id=wxID_ABOUTAUTOMODELSTATICTEXT2,
              label=u'E-mail: automodel@gmail.com', name='staticText2',
              parent=self, pos=wx.Point(88, 80), size=wx.Size(203, 17),
              style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButtonOkButton(self, event):
        self.Destroy()

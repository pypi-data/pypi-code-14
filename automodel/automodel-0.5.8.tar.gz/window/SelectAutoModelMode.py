#Boa:Dialog:SelectAutoModelMode

import wx
from model.AutoModelMode import AutoModelMode
def create(parent):
    return SelectAutoModelMode(parent)

[wxID_SELECTAUTOMODELMODE, wxID_SELECTAUTOMODELMODEBUTTONCANCEL, 
 wxID_SELECTAUTOMODELMODEBUTTONOK, 
 wxID_SELECTAUTOMODELMODERADIOBUTTONCLIENTSERVER, 
 wxID_SELECTAUTOMODELMODERADIOBUTTONOFFLINE, 
 wxID_SELECTAUTOMODELMODESTATICBOX1, wxID_SELECTAUTOMODELMODESTATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(7)]

class SelectAutoModelMode(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_SELECTAUTOMODELMODE,
              name=u'SelectAutoModelMode', parent=prnt, pos=wx.Point(461, 315),
              size=wx.Size(353, 240), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Select AutoModel Mode')
        self.SetClientSize(wx.Size(353, 240))

        self.radioButtonClientServer = wx.RadioButton(id=wxID_SELECTAUTOMODELMODERADIOBUTTONCLIENTSERVER,
              label=u'Internet Mode', name=u'radioButtonClientServer',
              parent=self, pos=wx.Point(104, 96), size=wx.Size(192, 32),
              style=0)
        self.radioButtonClientServer.SetValue(True)

        self.radioButtonOffline = wx.RadioButton(id=wxID_SELECTAUTOMODELMODERADIOBUTTONOFFLINE,
              label=u'Offline Mode', name=u'radioButtonOffline', parent=self,
              pos=wx.Point(104, 136), size=wx.Size(208, 32), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_SELECTAUTOMODELMODESTATICBOX1,
              label=u'', name='staticBox1', parent=self, pos=wx.Point(16, 72),
              size=wx.Size(320, 112), style=0)

        self.buttonCancel = wx.Button(id=wxID_SELECTAUTOMODELMODEBUTTONCANCEL,
              label=u'Cancel', name=u'buttonCancel', parent=self,
              pos=wx.Point(56, 200), size=wx.Size(85, 27), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_SELECTAUTOMODELMODEBUTTONCANCEL)

        self.buttonOK = wx.Button(id=wxID_SELECTAUTOMODELMODEBUTTONOK,
              label=u'OK', name=u'buttonOK', parent=self, pos=wx.Point(224,
              200), size=wx.Size(85, 27), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_SELECTAUTOMODELMODEBUTTONOK)

        self.staticText1 = wx.StaticText(id=wxID_SELECTAUTOMODELMODESTATICTEXT1,
              label=u'AutoModel can be utilized in Internet mode or in offline mode. The offline mode is only available  if all dependencies are installed.',
              name='staticText1', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(336, 64), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.automodelMode = AutoModelMode()
        if not self.automodelMode.offline_mode_is_ready():
          self.radioButtonOffline.Enable(False)

    def OnButtonCancelButton(self, event):
        self.Destroy()

    def OnButtonOKButton(self, event):
        if self.radioButtonClientServer.GetValue():
          self.automodelMode.online_mode()
        elif self.radioButtonOffline.GetValue():
          self.automodelMode.offline_mode()
        else:
          pass
        self.Close()

    # def OnSelectAutoModelModeClose(self, event):
    #         self.Destroy()
    #         pass